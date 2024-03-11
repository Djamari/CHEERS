import config as cfg
import numpy as np
from statesegmentation import GSBS
import multiprocessing

nr_parallel_jobs = 10
ROIs = cfg.ROIs

def fit_GSBS(GSBS_obj, savename):
    GSBS_obj.fit()
    np.save(savename, GSBS_obj)

processes = []
for run in cfg.run_numbers:
    print("Start Run " + str(run))
    for ROI in ROIs:
        # Load data of this ROI
        data = np.load(cfg.dir_preGSBS + 'preGSBS_run-'  + str(run) + '_' + ROI + '_mean.npy')

        # Create GSBS object and savename
        GSBS_obj = GSBS(x=data, kmax=int(data.shape[0] * cfg.kmax_ratio), finetune=cfg.finetune, statewise_detection=True)
        savename = cfg.dir_GSBS_ROIs + 'GSBS_run' + str(run) + '_finetune' + str(cfg.finetune) + '_' + ROI + '.npy'

        # Start GSBS fit in parallel
        p = multiprocessing.Process(target=fit_GSBS, args=(GSBS_obj, savename))
        processes.append(p)
        p.start()

        # If the maximum number of parallel jobs is reached, wait for the current jobs to be done
        if len(processes) >= nr_parallel_jobs:
            for process in processes:
                process.join()
            processes = []




