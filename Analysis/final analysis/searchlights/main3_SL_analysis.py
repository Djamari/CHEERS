from multiprocessing import set_start_method, Process
set_start_method('spawn', force=True)
import sys
sys.path.append("..")
from ROIs.main4_match import get_partial_correlation, get_annotations_matrix
from support.annotations import *
from support.funcs import *
from os.path import exists
import nibabel as nib
import numpy as np


savedir = cfg.dir_fig + 'Analysis results/searchlights/'
save_intermediate_results = '/home/djaoet/wrkgrp/Djamari/StudyForrest/intermediate_results/'
SL_dir = '/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/masks/searchlights/'
dir_SL_GSBS = cfg.dir_GSBS_SLs
nr_parallel_jobs = 10

analyses = cfg.analyses

stride=cfg.SL_stride
radius=cfg.SL_radius
min_vox=cfg.SL_min_vox
params_name = 'stride' + str(stride) + '_' + 'radius' + str(radius) + '_minvox' + str(min_vox)

# Get affine information for plotting
img = nib.load('/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/func/sub-01/ses-movie/func/sub-01_movie_run-1_hyperaligned.nii')
affine = img.affine


def get_partial_correlation_and_save(strengths_allRuns, annotation_matrix, savename):
    Rs = get_partial_correlation(strengths_allRuns, annotation_matrix, return_p=False)
    ps, match_null = permutation_test(strengths_allRuns, get_partial_correlation, "None", False, annotation_matrix, False)
    max_cor = get_max_correlation(strengths_allRuns, annotation_matrix, 0)
    np.save(savename + "R", Rs)
    np.save(savename + "p", ps)
    np.save(savename + "match_null", match_null)
    np.save(savename + "maxRs", max_cor)

def main_analysis_correlation(searchlights):

    for analysis_label in analyses.keys():
        print("STARTING ANALYSIS " + analysis_label)
        covariate_labels = cfg.analyses[analysis_label]
        all_labels = [analysis_label]
        all_labels.extend(covariate_labels)
        print("Covariates: " + str(covariate_labels))

        if 'mfcc' in all_labels:
            load_audio = True
        else:
            load_audio = False

        processes = []

        # Get annotations
        annotations_allRuns = dict((run, []) for run in cfg.run_numbers)
        for run_nr in cfg.run_numbers:
            annotations = Annotations(run_nr, cfg.delay, load_audio=load_audio)
            annotations_overTime = annotations.get_changes_overTime(all_labels)

            # Store current annotations
            annotations_allRuns[run_nr] = annotations_overTime

        # Transform to annotation matrix
        annotation_matrix = get_annotations_matrix(annotations_allRuns)

        # Perform analysis per SL
        for SL_idx, voxel_indices in enumerate(tqdm(searchlights)):
            # Skip if already done
            filename = save_intermediate_results + "analysis_" + analysis_label + "SL" + str(SL_idx) + "_maxRs.npy"
            if exists(filename):
                continue

            strengths_allRuns = dict((run, []) for run in cfg.run_numbers)

            for run_nr in cfg.run_numbers:

                # Load GSBS object
                filename = dir_SL_GSBS + 'GSBS_run' + str(run_nr) + '_' + params_name + '_SL' + str(SL_idx) + '.npy'
                GSBS_results = np.load(filename, allow_pickle=True).item()
                strengths = GSBS_results.get_strengths()

                strengths_allRuns[run_nr].extend(strengths) # add strength one time only
                strengths_allRuns[run_nr] = np.asarray(strengths_allRuns[run_nr])


            # Do one full run analysis (per label)
            save_prefix = save_intermediate_results  + "analysis_" + analysis_label + "SL" + str(SL_idx) + "_"
            p = Process(target=get_partial_correlation_and_save, args=(strengths_allRuns, annotation_matrix, save_prefix))
            processes.append(p)
            p.start()

            # To avoid too many jobs at the same time
            if len(processes) >= nr_parallel_jobs:
                for process in processes:
                    process.join()
                processes = []

        # Finish processes
        for process in processes:
            process.join()


if __name__ == '__main__':


    # Get searchlight information
    coordinates = np.load(SL_dir + 'SL_voxelCoordinates_' + params_name + '.npy', allow_pickle=True)
    searchlights = np.load(SL_dir + 'SL_voxelsIndices_' + params_name + '.npy', allow_pickle=True)

    # Perform analysis (comment out if just wanting to plot)
    main_analysis_correlation(searchlights)

    print("Start plotting")
    Rs_SLs_allRuns = np.zeros((len(searchlights), len(analyses.keys())))
    ps_SLs_allRuns = np.zeros((len(searchlights), len(analyses.keys())))

    for label_idx, analysis_label in enumerate(analyses.keys()):  # One figure per label
        for SL_idx, voxel_indices in enumerate(tqdm(searchlights)):
            Rs = np.load(save_intermediate_results  + "analysis_" + analysis_label + "SL" + str(SL_idx) + "_R.npy")
            ps = np.load(save_intermediate_results  + "analysis_" + analysis_label + "SL" + str(SL_idx) + "_p.npy")

            Rs_SLs_allRuns[SL_idx][:] = Rs
            ps_SLs_allRuns[SL_idx][:] = ps



        # Compute which p-value survives correction
        SLs_significant_corrected, highest_p = BH_correction_Sls(ps_SLs_allRuns[:, label_idx],np.arange(ps_SLs_allRuns[:, label_idx].shape[0]))
        np.save(savedir + "SL_survival_" + analysis_label, SLs_significant_corrected)

        # Gather info
        x_max, y_max, z_max, T = img.shape
        counter = np.zeros((x_max, y_max, z_max))
        match_sum = np.zeros((x_max, y_max, z_max))
        p_total = np.zeros((x_max, y_max, z_max))
        sigvox_uncorrected = np.zeros((x_max, y_max, z_max))
        sigvox_corrected = np.zeros((x_max, y_max, z_max))

        for SL_idx, voxel_indices in enumerate(tqdm(searchlights)):
            match = Rs_SLs_allRuns[SL_idx][label_idx]

            for vox in voxel_indices:
                x, y, z = coordinates[vox]
                counter[x, y, z] += 1
                match_sum[x, y, z] += match
                p_total[x,y,z] += ps_SLs_allRuns[SL_idx,label_idx]


        # Take mean across searchlights
        mean_match = np.divide(match_sum, counter)
        p_average = np.divide(p_total, counter)

        # Create map of <0.05 (uncorrected)
        idx_keep = np.where(p_average < 0.05)
        mean_match_thres_uncorrected = np.zeros_like(mean_match) * np.nan
        mean_match_thres_uncorrected[idx_keep] = mean_match[idx_keep]

        # Create corrected map
        idx_keep = np.where(p_average <= highest_p)
        mean_match_thres_corrected = np.zeros_like(mean_match) * np.nan
        mean_match_thres_corrected[idx_keep] = mean_match[idx_keep]

        # Convert to nifti
        map_nifti = nib.Nifti1Image(mean_match, affine)
        nib.save(map_nifti, savedir + 'analysis_' + analysis_label + '_Rs.nii')

        # Threshold at p<0.05
        map_nifti = nib.Nifti1Image(mean_match_thres_uncorrected, affine)
        nib.save(map_nifti, savedir +  'analysis_' + analysis_label + '_Rs_thresholded_uncorrected.nii')

        # Threshold based on correction
        map_nifti = nib.Nifti1Image(mean_match_thres_corrected, affine)
        nib.save(map_nifti, savedir +  'analysis_' + analysis_label + '_Rs_thresholded_corrected.nii')

