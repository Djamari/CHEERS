import numpy as np
import matplotlib.pyplot as plt
import config as cfg
from support.funcs import p_to_arterisks
import seaborn as sns

sns.set()

dir_results = cfg.dir_fig + 'Analysis results/extra/'
dir_save = cfg.dir_fig + 'Analysis results/extra/'

# Figure parameters
barwidth= 0.25
cm = 1/2.54  # centimeters in inches
csfont={'fontname': 'DejaVuSerifCondensed'}
fontsize = 20

def label_to_title(label):
    titles = {
        'normdiff': 'Low-level visual features',
        'shot': 'Shots',
        'location3': 'Small-scale locations',
        'location2': 'Large-scale locations',
        'event': 'Events'
    }
    return titles[label]

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


    name = "normal_correlation_ROIs_"
    matches = np.load(dir_results + name + '_matches.npy', allow_pickle=True).item()

    for ROI in cfg.ROIs:
        this_value = np.asarray(list(matches[ROI].values()))
        this_max = np.max(this_value)
        this_min = np.min(this_value)

        ymin = np.min((this_min, ymin))
        ymax = np.max((this_max, ymax))

    # Extract numbers and plot; one figure per analysis, but in subplots
    analysis =  ["normdiff", "location3", "location2", "event"] # Settle order
    nr_labels = len(analysis)

    matches = np.load(dir_results + name + '_matches.npy', allow_pickle=True).item()

    p_values = np.load(dir_results + name + '_p_uncorrected.npy', allow_pickle=True).item()
    significant_labels = np.load(dir_results + name + '_significant_labels_corrected.npy', allow_pickle=True).item()

    f, ax = plt.subplots(1,nr_labels, figsize=(22 * cm*2,5 * cm*2))
    ys_all = [] # to later compute max and min
    for label_idx, label in enumerate(analysis):
        x_labels = []
        plt.sca(ax[label_idx])
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
            if label in significant_labels[ROI]:
                p_text = p_to_arterisks(p_values[ROI][label])
            elif p_values[ROI][label] < 0.05:
                p_text = "o"
            else:
                p_text = None

            # Bars
            plt.bar(x, y, width=barwidth, color=cfg.ROI_colors[ROI])

            # P values
            plt.text(x, y, p_text, ha='center', fontsize='large')

        ax[label_idx].xaxis.grid(False)
        plt.title(label_to_title(label), fontsize=fontsize)

        # Layout
        plt.axhline(0, color='k')
        plt.xlim([-0.5,2.5])
        plt.xticks(np.arange(len(cfg.ROIs)/2), x_labels, fontsize=fontsize)

    # Compute ylimits and set numbers
    y_min = -0.001 # set ymin to 0
    y_max = np.max(ys_all) + 0.01
    for a_idx, a in enumerate(ax):
        plt.sca(a)
        plt.ylim([y_min, y_max])
        if a_idx == 0:
            plt.ylabel("Pearson's r", fontsize=fontsize)
            plt.yticks(fontsize=fontsize)
        else:
            a.set_yticklabels([])

    plt.tight_layout()

    # Save
    plt.savefig(dir_save + "normal_correlation_ROI" + '.eps')
    plt.savefig(dir_save + "normal_correlation_ROI" + '.svg')
    plt.savefig(dir_save + "normal_correlation_ROI" + '.png')

