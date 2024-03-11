from statesegmentation import GSBS
import numpy as np
import config as cfg
import multiprocessing


nr_parallel_jobs = 25

SL_dir = '/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/masks/searchlights/'
save_dir = cfg.dir_GSBS_SLs


stride=cfg.SL_stride
radius=cfg.SL_radius
min_vox=cfg.SL_min_vox
params_name = 'stride' + str(stride) + '_' + 'radius' + str(radius) + '_minvox' + str(min_vox)

coordinates = np.load(SL_dir + 'SL_voxelCoordinates_' + params_name + '.npy',allow_pickle=True)
searchlights = np.load(SL_dir + 'SL_voxelsIndices_'+ params_name + '.npy',allow_pickle= True)


def GSBS_SL(data_SL, SL_idx, run_nr):
    GSBS_SL_obj = GSBS(x=data_SL, kmax=int(data_SL.shape[0] * cfg.kmax_ratio), finetune=1, blocksize=50, statewise_detection=True)
    GSBS_SL_obj.fit(False)
    savename = save_dir + 'GSBS_run' + str(run_nr) + '_' + params_name + '_SL' + str(SL_idx)
    np.save(savename, GSBS_SL_obj)
    return

if __name__ == '__main__':
    processes = []

    for run_nr in cfg.run_numbers:
        print("Start GSBS Run " + str(run_nr))

        # Load mean data of this run
        data = np.load(cfg.dir_preGSBS +  'preGSBS_run-' + str(run_nr) + '_wholeBrain_mean.npy', allow_pickle=True)

        # Loop through all search lights
        for SL_idx, voxel_indices in enumerate(searchlights):

            # Get data of this searchlight
            vox_coords = coordinates[voxel_indices]
            data_SL = []
            for x,y,z in vox_coords:
                data_SL.append(data[x,y,z,:])
            data_SL = np.transpose(np.asarray(data_SL)) # Go to time x voxel

            # Start job
            p = multiprocessing.Process(target=GSBS_SL, args=(data_SL,SL_idx, run_nr,))
            processes.append(p)
            p.start()

            # To avoid too many jobs at the same time
            if len(processes) >= nr_parallel_jobs:
                for process in processes:
                    process.join()
                processes = []


