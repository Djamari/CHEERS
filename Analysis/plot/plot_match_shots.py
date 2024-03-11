import numpy as np
import matplotlib.pyplot as plt
import config as cfg
from support.funcs import p_to_arterisks
import seaborn as sns
import nibabel as nib
from nilearn import plotting

sns.set()
dir_results_ROI = cfg.dir_fig
dir_results_wholebrain = cfg.dir_fig + 'Analysis results/extra/searchlights/'
dir_save = cfg.dir_fig + 'Analysis results/shots/'

# Figure parameters
barwidth= 0.3
cm = 1/2.54  # centimeters in inches
csfont={'fontname': 'DejaVuSerifCondensed'}
fontsize = 20
fontsize_numbers = 15



def ROI_to_text(ROI):
    texts = {
        'VIS_L': 'EV',
        'VIS_R': 'EV',
        'PPA_L': 'PPA',
        'PPA_R': 'PPA',
        'RSC_L': 'RSC',
        'RSC_R': 'RSC'
    }
    return texts[ROI]

if __name__ == "__main__":
    f, ax = plt.subplots(1,2,figsize=(13.5 * cm*2,5 * cm*2))
    label = 'shot'

    ys_all = [] # to later compute max and min

    for f_idx, name in enumerate(['Analysis results/ROI match/analysis_all', 'Analysis results/extra/normal_correlation_ROIs_']):

        matches = np.load(dir_results_ROI + name + '_matches.npy', allow_pickle=True).item()
        matches_max = np.load(dir_results_ROI + name + '_matches_max.npy', allow_pickle=True).item()
        p_values = np.load(dir_results_ROI + name + '_p_uncorrected.npy', allow_pickle=True).item()
        significant_labels = np.load(dir_results_ROI + name + '_significant_labels_corrected.npy', allow_pickle=True).item()

        x_labels = []
        plt.sca(ax[f_idx])
        for ROI_idx, ROI in enumerate(cfg.ROIs):
            # Compute x-value
            if ROI_idx%2 == 0:
                x_labels.append(ROI_to_text(ROI))
                x = int(ROI_idx/2) - barwidth/2
            else:
                x = int(ROI_idx / 2) + barwidth / 2

            # Compute relative correlation
            y = matches[ROI][label] / matches_max[ROI][label]
            ys_all.append(y)

            # Compute p text
            if p_values[ROI][label] < 0.05:
                p_text = p_to_arterisks(p_values[ROI][label])
            else:
                p_text = None

            # Bars
            # plt.bar(x, y, width=barwidth, edgecolor='black', color=cfg.ROI_colors[ROI])
            plt.bar(x, y, width=barwidth, color=cfg.ROI_colors[ROI])



            # p values in gray if not surviving correction for multiple comparisons
            if p_values[ROI][label] < 0.05 and label not in significant_labels[ROI]:
                plt.text(x, y, 'o', ha='center', fontsize='large')
            else:
                plt.text(x, y, p_text, ha='center', fontsize='large')
        ax[f_idx].xaxis.grid(False)

        if 'normal' in name:
            plt.title("Shot analysis, Pearson's R", fontsize=fontsize)
        else:
            plt.title("Shot analysis, partial correlation", fontsize=fontsize)

        # Layout
        plt.hlines(0,-1, np.max(x) + 1, 'k')
        plt.xlim([-0.5,2.5])
        plt.xticks(np.arange(len(cfg.ROIs)/2), x_labels, fontsize=fontsize_numbers)

    # Compute ylimits and set numbers
    y_min = np.min(ys_all) - 0.01
    y_max = np.max(ys_all) + 0.02
    for a_idx, a in enumerate(ax):
        plt.sca(a)
        plt.ylim([y_min, y_max])

        plt.ylabel('Relative R', fontsize=fontsize)
        plt.yticks(fontsize=fontsize_numbers)

    # Save
    plt.tight_layout()
    plt.savefig(dir_save + "shots_ROI.svg")
    plt.savefig(dir_save + "shots_ROI.png")

    ### Whole-brain
    # Prepare uncorrected
    file = 'analysis_normalR_' + label + '_Rs_relative_thresholded_uncorrected.nii'
    img = nib.load(dir_results_wholebrain + file)
    arr_binary = (img.get_fdata() > 0).astype(int)
    img_binary = nib.Nifti1Image(arr_binary, img.affine)

    MNI_coords = (5,-77,6)

    # Plot
    display = plotting.plot_roi(img_binary, axes=ax[2], cut_coords=MNI_coords, display_mode='tiled',
                                bg_img=cfg.background_image, alpha=0.65, draw_cross=False)
    display.add_overlay(dir_results_wholebrain + 'analysis_normalR_' + label + '_Rs_relative__thresholded_corrected.nii',
                        colorbar=True, alpha=1, cmap='autumn')
    for ROI in cfg.ROIs:
        display.add_contours(cfg.dir_ROI + ROI + '.nii', colors='k', levels=[3.0], linewidths=1, alpha=1.0)


    # Save
    plt.tight_layout()
    plt.savefig(dir_save + "shots.svg")
    plt.savefig(dir_save + "shots.png")