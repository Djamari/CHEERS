import config as cfg
import numpy as np
from nltools.data import Brain_Data
from tqdm import tqdm

dir_ROI = cfg.dir_ROI
ROIs = cfg.ROIs
dir_preGSBS = cfg.dir_preGSBS

for run in range(1,9):
    print("Start run " + str(run))

    # Load data
    filename = dir_preGSBS + 'preGSBS_run-' + str(run) + '_wholeBrain_mean.npy'
    data_wholebrain = np.load(filename)

    for ROI in tqdm(ROIs):
        # Load ROI mask
        mask = Brain_Data(dir_ROI + ROI + '.nii', mask=dir_ROI + ROI + '.nii')
        affine = mask.to_nifti().affine

        # Get index values
        coords = np.where(mask.to_nifti().get_fdata() > 0)

        data_ROI = []
        # Mask whole brain data
        for voxel in range(coords[0].shape[0]):
            x,y,z = coords[0][voxel], coords[1][voxel], coords[2][voxel]
            data_ROI.append(data_wholebrain[x,y,z,:])


        # Save Time x Voxel data
        data_ROI = np.asarray(data_ROI).T
        np.save(dir_preGSBS + 'preGSBS_run-' + str(run) + '_' + ROI +  '_mean.npy', data_ROI)