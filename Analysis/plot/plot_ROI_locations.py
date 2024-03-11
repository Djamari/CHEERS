import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import config as cfg
from nilearn import plotting
from plot_match_per_ROI import ROI_to_text
from matplotlib.colors import ListedColormap

dir_save = cfg.dir_fig + 'Analysis results/descriptives/'

slices = [(12, -96, 9), # EV
          (27, -51, -12), # PPA
        (-15, -54, 12), # RSC
        ]

f, ax = plt.subplots(3, 1, figsize=(20, 20))
for slice, MNI_coords in enumerate(slices):
    display = None

    for ROI in cfg.ROIs:
        filename = cfg.dir_ROI + ROI + '.nii'
        img = nib.load(filename)

        c = cfg.ROI_colors[ROI]
        cmap_colors = [c, c]

        if display == None:
            display = plotting.plot_stat_map(filename, cmap=ListedColormap(cmap_colors), axes=ax[slice], cut_coords=MNI_coords, display_mode='ortho',  bg_img=cfg.background_image, alpha=1, draw_cross=True, colorbar=False)
        else:
            display.add_overlay(filename,  colorbar=False, alpha=1, cmap=ListedColormap(cmap_colors))



# Add custom legend
plt.sca(ax[0])
patches_list = []
for ROI in cfg.ROIs:
    if 'L' in ROI:
        label = 'left ' + ROI_to_text(ROI)
    else:
        label = 'right ' + ROI_to_text(ROI)
    patches_list.append(patches.Patch(color=cfg.ROI_colors[ROI], label=label))
plt.legend(handles=patches_list, loc='best')

# Save
display.savefig(dir_save + "ROIs.png")
display.savefig(dir_save + "ROIs.svg")