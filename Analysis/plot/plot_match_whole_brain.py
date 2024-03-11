import nibabel as nib
import config as cfg
from nilearn import plotting
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib as mpl

debug_txt = ""
dir_save = cfg.dir_fig + 'Analysis results/searchlights/paper/' + debug_txt
dir_data = cfg.dir_fig + 'Analysis results/searchlights/'

# Get vmin and vmax
vmin = 1000
vmax= -1000
for label in cfg.analyses.keys():
    if label == 'shot' or label == 'location2':
        # Skip because 1) nothing significant and 2) part of extra analysis
        continue

    file = 'analysis_' + label + '_Rs_relative__thresholded_corrected.nii'
    data = nib.load(dir_data + file).get_fdata()
    data[np.where(data==0)] = np.nan
    vmin = min(vmin,np.nanmin(data))
    vmax = max(vmax, np.nanmax(data))

for label in cfg.analyses.keys():
    if label == 'shot':
        # Skip because 1) nothing significant and 2) part of extra analysis
        continue

    name = 'whole_brain_thresholded_uncorrected_' + label
    filename_solid = name + '.nii'

    slices = cfg.whole_brain_slices[label]
    f, ax = plt.subplots(2, 1, figsize=(20, 20))
    output_name = debug_txt + 'whole_brain_' + label
    for slice, MNI_coords in enumerate(slices):
        if label == 'event':
            mode = 'x'
            MNI_coords = np.arange(-60, 61, 10)
            plt.figure()
            axes=None
        else:
            mode = 'ortho'
            axes = ax[slice]
        display = plotting.plot_roi(dir_data + filename_solid, axes=axes, cut_coords=MNI_coords, display_mode=mode,  bg_img=cfg.background_image, alpha=0.65, draw_cross=False)

        display.add_overlay(dir_data + 'analysis_' + label + '_Rs_relative__thresholded_corrected.nii',  colorbar=True, alpha=1, cmap='autumn', vmin=vmin, vmax=vmax)
        for ROI in cfg.ROIs:
            display.add_contours(cfg.dir_ROI + ROI + '.nii', colors='k', levels=[3.0], linewidths=1, alpha = 1.0)

    display.savefig(dir_save + output_name + "_solid.png")
    display.savefig(dir_save + output_name + "_solid.svg")

# Customized colorbar
fig, ax = plt.subplots(figsize=(1.1, 3))

cmap = mpl.cm.autumn
norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
tick_min = np.round(vmin,2)
tick_max = np.round(vmax,2)
cbar_obj = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
             cax=ax, orientation='vertical', ticks = np.arange(tick_min,tick_max+0.01,0.01))
cbar_obj.set_label("Relative R", labelpad=5)

cbar_obj.set_ticklabels(np.round(np.arange(tick_min,tick_max,0.01),2).astype(str))
ax.yaxis.set_ticks_position('left')
plt.tight_layout()


plt.savefig(dir_save + "colorbar_partialR.png")
plt.savefig(dir_save + "colorbar_partialR.svg")