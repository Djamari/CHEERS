from support.annotations import *
import sys
sys.path.append("../..")
from support.partial_corr import  partial_corr_first_two_columns_only
from support.funcs import  permutation_test, Bonferroni_for_ROIs

save_dir = cfg.dir_fig + 'Analysis results/ROI match/'
ROIs = cfg.ROIs

def get_full_timeline(timeline):
    # Given a dictionary with each key being a run number, concatenate all elements to create one timeline
    timeline_all = []
    for run_nr in timeline.keys():
        timeline_all.extend(timeline[run_nr])
    return timeline_all

def get_annotations_matrix(annotations):
    # Per label, create full timeline and to create one big annotation matrix to be used in computing partial correlation
    for run_nr in cfg.run_numbers:
        # If alexnet is involved, some additional steps are necessary because of the various layers
        if 'alexnet' in annotations[run_nr].keys():
            for l_idx, label in enumerate(annotations[run_nr].keys()):
                if l_idx == 0:
                    to_add = np.asarray(list(annotations[run_nr][label])).T
                elif label == 'alexnet':
                    to_add = np.column_stack((to_add, np.asarray(list(annotations[run_nr]['alexnet'])).T))
                else:
                    to_add = np.column_stack((to_add,np.asarray(list(annotations[run_nr][label])).T))
        else:
            to_add = np.asarray(list(annotations[run_nr].values())).T

        # Store current run annotations
        if run_nr == 1: # First run
            timeline_label = to_add
        else:
            timeline_label = np.row_stack((timeline_label, to_add))

    # Add intersect
    annotation_matrix = np.column_stack((timeline_label, np.ones(timeline_label.shape[0])))
    return annotation_matrix

def get_partial_correlation(timeline, annotation_matrix, return_p):
     # ASSUMPTION: annotation of interest is the very first column in annotation matrix

    # Create full timeline
    timeline_all = np.asarray(get_full_timeline(timeline))

    # Merge strength timeline and annotation matrix into obs
    obs = np.column_stack((timeline_all, annotation_matrix))

    # Only compute partial correlation between first entry of obs and everything else
    R, p = partial_corr_first_two_columns_only(obs)

    # Return list version for compatibility with permutation function
    if return_p:
        # Skip the intersect value; only first row for cor with GSBS (as list for later use)
        return [R], [p]
    else:
        return [R]


def main_analysis():
    # Prepare dictionaries
    matches_ROIs_allAnalyses = dict((ROI, {}) for ROI in ROIs)
    p_ROIs_allAnalyses = dict((ROI, {}) for ROI in ROIs)

    # Loop through the various analyses (with a seperate annotation category of interest per analysis)
    for analysis_label in list(cfg.analyses.keys()):
        covariate_labels = cfg.analyses[analysis_label]
        all_labels = [analysis_label]
        all_labels.extend(covariate_labels)

        print("----------------------")
        print("Analysis: " + analysis_label)
        print("Covariates: " + str(covariate_labels))

        # Perform analysis per ROI
        for ROI in ROIs:
            print(ROI)

            # Loop through runs and gather all necessary information
            strengths_all = dict((run_nr, []) for run_nr in cfg.run_numbers)
            annotations_all = dict((run_nr, []) for run_nr in cfg.run_numbers)
            for run_nr in cfg.run_numbers:
                # Get annotations
                annotations = Annotations(run_nr, delay_s=cfg.delay)
                annotations_overTime = annotations.get_changes_overTime(all_labels)

                # Load GSBS object
                filename = cfg.dir_GSBS_ROIs + 'GSBS_run' + str(run_nr) + '_finetune' + str(cfg.finetune) + '_' + ROI + '.npy'
                GSBS_results = np.load(filename, allow_pickle=True).item()

                strengths = GSBS_results.get_strengths()

                # Store
                strengths_all[run_nr] = strengths
                annotations_all[run_nr] = annotations_overTime

            # Get actual match
            annotation_matrix = get_annotations_matrix(annotations_all)
            match_data = get_partial_correlation(strengths_all, annotation_matrix, return_p=False)

            # Permutation test
            savename = save_dir + 'nulldistr_' + ROI + '_run'
            ps, match_null = permutation_test(strengths_all, get_partial_correlation, savename, True, annotation_matrix, False)
            print("P = " + str(ps))
            print("r = " + str(match_data))

            # Store match and p value
            p_ROIs_allAnalyses[ROI][analysis_label] = ps
            matches_ROIs_allAnalyses[ROI][analysis_label] = match_data[0]

    # Save results
    np.save(save_dir + "analysis_all_p_uncorrected", p_ROIs_allAnalyses)
    np.save(save_dir + "analysis_all_matches", matches_ROIs_allAnalyses)

    # Correction for multiple comparisons (correcting for number of ROIs using Bonferroni)
    significant_labels_corrected = Bonferroni_for_ROIs(p_ROIs_allAnalyses)
    print(significant_labels_corrected)
    np.save(save_dir + "analysis_all_significant_labels_corrected",significant_labels_corrected)

if __name__ == '__main__':

    # Perform main analysis
    main_analysis()

