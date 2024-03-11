import matplotlib
from support.funcs import *

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

ROIs = cfg.ROIs

def plot_pvalues(load_dir):
    p_values = np.load(load_dir + "analysis_all_p_uncorrected.npy", allow_pickle=True).item()
    significant_labels = np.load(load_dir + "analysis_all_significant_labels_corrected.npy", allow_pickle=True).item()

    analyses = cfg.analyses
    nr_analyses = len(analyses.keys())

    to_plot_uncorrected = np.zeros((len(ROIs), nr_analyses))
    to_plot_corrected = np.zeros((len(ROIs), nr_analyses))
    for r_idx, ROI in enumerate(ROIs):
        to_plot_uncorrected[r_idx][np.asarray(p_values[ROI]) < 0.1] = 0.5
        to_plot_uncorrected[r_idx][np.asarray(p_values[ROI]) < 0.05] = 1

        for label_idx, label in enumerate(analyses.keys()):
            to_plot_corrected[r_idx][label_idx] = label in significant_labels[ROI]

    f, ax = plt.subplots(1,2)
    plt.sca(ax[0])
    plt.imshow(to_plot_uncorrected, vmin=0)
    plt.yticks(range(len(ROIs)), ROIs)
    plt.xticks(range(len(list(analyses.keys()))), list(analyses.keys()), rotation='vertical')
    plt.title('Uncorrected')

    plt.sca(ax[1])
    plt.imshow(to_plot_corrected, vmin=0)
    plt.yticks(range(len(ROIs)), ROIs)
    plt.xticks(range(len(list(analyses.keys()))), list(analyses.keys()), rotation='vertical')
    plt.title('Corrected')

    f.tight_layout()
    f.savefig(load_dir +"overview_pvalues.png")

def plot_matches(savedir):
    labels_analysis = list(cfg.analyses.keys())
    matches = np.load(savedir + "analysis_all_matches.npy", allow_pickle=True).item()
    matches_max = np.load(savedir + "analysis_all_matches_max.npy", allow_pickle=True).item()

    p_values = np.load(savedir + "analysis_all_p_uncorrected.npy", allow_pickle=True).item()
    significant_labels = np.load(savedir + "analysis_all_significant_labels_corrected.npy", allow_pickle=True).item()


    # Plot  match values with significance
    x = np.arange(len(matches[ROIs[0]]))
    f, ax = plt.subplots(len(ROIs), 1, figsize=(5, 15), sharex=True, sharey=True)
    for row_idx, ROI in enumerate(ROIs):
        max_value = matches_max[ROI]
        y = matches[ROI]/max_value
        ax[row_idx].bar(x, y)
        for p_idx, p in enumerate(p_values[ROI]):
            if labels_analysis[p_idx] in significant_labels[ROI]:
                ax[row_idx].text(x[p_idx], y[p_idx], p_to_arterisks(p), ha='center')
        ax[row_idx].set_title(ROI)
        ax[row_idx].axhline(0, color = 'k')
        if row_idx == 3:
            ax[row_idx].set_ylabel('Pearson R')
        if row_idx == len(ROIs) - 1:
            ax[row_idx].set_xticks(np.arange(len(labels_analysis)))
            ax[row_idx].set_xticklabels(labels_analysis)
    plt.tight_layout()
    plt.savefig(savedir +"analysis_matches")
    f.savefig(savedir + "analysis_matches.pdf",  transparent=True)





