import nibabel as nib
import config as cfg
from nilearn import plotting
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from matplotlib import cm

dir_save = cfg.dir_fig + 'Analysis results/searchlights/paper/'
dir_data = cfg.dir_fig + 'Analysis results/searchlights/'
dir_cope = cfg.dir_root + 'Scripts/Preprocessing/create masks/functional_3mm/results_cope3/'
label = 'location3'
theta = 3.79 # Based on SPM results

name = 'whole_brain_thresholded_corrected_' + label
filename_solid_data = name + '_binary.nii'

# Create binarized bersion of corrected values, to show in red
corrected_continuous = nib.load(dir_data + 'analysis_' + label + '_Rs_thresholded_corrected.nii')
data_binarized_results = (corrected_continuous.get_fdata() > 0).astype(int)
affine = corrected_continuous.affine
nib.save(nib.Nifti1Image(data_binarized_results, affine), dir_data + filename_solid_data)

# Binarize cope3
filename_solid_cope3 = 'cope3_binary.nii'
continuous = nib.load(dir_cope + 'spmT_0001.nii')
data_binarized_cope = (continuous.get_fdata() > theta).astype(int)
affine = continuous.affine
nib.save(nib.Nifti1Image(data_binarized_cope, affine), dir_data + filename_solid_cope3)

# Save binarized overlap
filename_solid_overlap = 'cope3_binary_overlap.nii'
continuous = data_binarized_cope + data_binarized_results
data_binarized_overlap = (continuous > 1).astype(int)
nib.save(nib.Nifti1Image(data_binarized_overlap, affine), dir_data + filename_solid_overlap)

slices = cfg.whole_brain_slices[label]
plt.figure()
output_name = 'OPA_cope3_theta' + str(theta)
MNI_coords = (-30,-90,15)
mode = 'ortho'
axes = None

# Create custom colormap (for which perhaps the binarization was not necessary but oh well)
viridis = cm.get_cmap('viridis', 256)
new_colors = viridis(np.linspace(0,1,256))
new_colors[:, :3] =np.asarray([234,61,37])/256 # red

display = plotting.plot_roi(dir_data + filename_solid_data, axes=axes, cut_coords=MNI_coords, display_mode=mode, bg_img=cfg.background_image, alpha=1, draw_cross=False,cmap = ListedColormap(new_colors))

# Plot thresholded cope results
new_colors = new_colors.copy()
new_colors[:, :3]  =  np.asarray([22,60,245])/256 # blue
display.add_overlay(dir_data + filename_solid_cope3,  colorbar=False, alpha=1, cmap = ListedColormap(new_colors))

# Plot overlap in purple
new_colors = new_colors.copy()
new_colors[:, :3]  = np.asarray([255,255,85])/256 # overlap color
display.add_overlay(dir_data + filename_solid_overlap,  colorbar=False, alpha=1, cmap = ListedColormap(new_colors))

# Add ROI contours
for ROI in cfg.ROIs:
    display.add_contours(cfg.dir_ROI + ROI + '.nii', colors='k', levels=[3.0], linewidths=1, alpha = 1)

plt.tight_layout()
display.savefig(dir_save + output_name + ".png")
display.savefig(dir_save + output_name + ".svg")


