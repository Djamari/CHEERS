import nibabel as nib
import numpy as np
from tqdm import tqdm
import config as cfg
import os

data_dir = cfg.dir_rawData
save_dir = cfg.dir_preGSBS

# Get list of subjects
allfiles = os.listdir(data_dir)
namelist=[]
for names in allfiles:
    if names.startswith("sub") and not names.endswith("phantom"):
        namelist.append(names)
namelist.sort()

# Loop through runs
for run_nr in range(1,9):
    print("Starting run " + str(run_nr))

    # Load data of all subjects
    data_allSubs = []
    for subject in tqdm(namelist):
        img = nib.load(data_dir + subject + '/ses-movie/func/' + subject + '_movie_run-' + str(run_nr) + '_hyperaligned.nii')
        data_allSubs.append(img.get_fdata())

    # Take average and save
    print("Saving...")
    data_mean = np.mean(np.asarray(data_allSubs), axis=0)
    np.save(save_dir + 'preGSBS_run-' + str(run_nr) + '_wholeBrain', data_mean)
    print("Done")