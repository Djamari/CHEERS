import numpy as np
import matplotlib.pyplot as plt
import config as cfg
from support.funcs import p_to_arterisks
import seaborn as sns


sns.set()
dir_results = cfg.dir_fig + 'Analysis results/ROI match/'
dir_save = cfg.dir_fig + 'Analysis results/ROI match/paper/'

annotation_order = ['normdiff', 'location3', 'location2', 'normdiff'] # Normdiff twice to have same subplot width as before. This extra subfigure should be ignored.

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
    # Determine ymin and ymax
    ymin = 100
    ymax = 0

    name = 'analysis_all'
    matches = np.load(dir_results + name + '_matches.npy', allow_pickle=True).item()
    p_values = np.load(dir_results + name + '_p_uncorrected.npy', allow_pickle=True).item()
    significant_labels = np.load(dir_results + name + '_significant_labels_corrected.npy', allow_pickle=True).item()

    for ROI in cfg.ROIs:
        this_value = np.asarray(list(matches[ROI].values()))
        this_max = np.max(this_value)
        this_min = np.min(this_value)

        ymin = np.min((this_min, ymin))
        ymax = np.max((this_max, ymax))

    # Extract numbers and plot; one figure per analysis, but in subplots
    nr_labels = len(annotation_order)


    f, ax = plt.subplots(1,nr_labels, figsize=(22 * cm*2,5 * cm*2))
    ys_all = [] # to later compute max and min
    for l_idx, label in enumerate(annotation_order):
        x_labels = []
        plt.sca(ax[l_idx])
        for ROI_idx, ROI in enumerate(cfg.ROIs):
            # Compute x-value
            if ROI_idx%2 == 0:
                x_labels.append(ROI_to_text(ROI))
                x = int(ROI_idx/2) - barwidth/2
            else:
                x = int(ROI_idx / 2) + barwidth / 2

            # Compute relative correlation
            y = matches[ROI][label]
            ys_all.append(y)

            # Compute p text
            if p_values[ROI][label] < 0.05:
                p_text = p_to_arterisks(p_values[ROI][label])
            else:
                p_text = None

            # Bars
            plt.bar(x, y, width=barwidth, color=cfg.ROI_colors[ROI])



            #  p values as circle if not surviving correction for multiple comparisons
            if p_values[ROI][label] < 0.05 and label not in significant_labels[ROI]:
                plt.text(x, y, 'o', ha='center', fontsize='large')
            else:
                plt.text(x, y, p_text, ha='center', fontsize='large')
        ax[l_idx].xaxis.grid(False)


        plt.title(cfg.label_to_title[label], fontsize=fontsize)

        # Layout
        plt.hlines(0,-1, nr_labels + 1, 'k')
        plt.xlim([-0.5,2.5])
        plt.xticks(np.arange(len(cfg.ROIs)/2), x_labels, fontsize=fontsize_numbers)

        # Compute ylimits and set numbers
        y_min = np.min(ys_all) - 0.01
        y_max = np.max(ys_all) + 0.01
        for a_idx, a in enumerate(ax):
            plt.sca(a)
            plt.ylim([y_min, y_max])
            if a_idx == 0:
                plt.ylabel('Partial r', fontsize=fontsize)
                plt.yticks(fontsize=fontsize_numbers)
            else:
                a.set_yticklabels([])
        plt.tight_layout()

    # Save
    plt.savefig(dir_save + "ROI_analysis.eps")
    plt.savefig(dir_save + "ROI_analysis.svg")
    plt.savefig(dir_save + "ROI_analysis.png")
