from mpl_toolkits.axes_grid1 import make_axes_locatable

from support.annotations import *
from support.funcs import *


import sys
sys.path.append("../..")


save_dir = cfg.dir_fig + 'annotations/'

ROI_label_to_ylabel = {
    'PPA_L': 'PPA left',
    'PPA_R': 'PPA right',
    'RSC_L': 'RSC left',
    'RSC_R': 'RSC right',
    'VIS_L': 'EV left',
    'VIS_R': 'EV right',
}

def plot_timelines(labels, run_nr):

    # Get and plot annotations
    matrix_all = np.zeros((len(labels), cfg.nTRs[run_nr])) * np.nan
    annotations = Annotations(run_nr, delay_s = cfg.delay).get_changes_overTime()

    l_idx_ROIs = []
    for l_idx, label in enumerate(labels):
        if label in cfg.ROIs:
            # Get ROI timelines
            filename = cfg.dir_GSBS_ROIs + 'GSBS_run' + str(run_nr) + '_finetune' + str(
                cfg.finetune) + '_' + label + '.npy'
            GSBS_results = np.load(filename, allow_pickle=True).item()
            matrix_all[l_idx,:] = GSBS_results.get_strengths()
            l_idx_ROIs.append(l_idx)
        else:
            # Get annotation timelines
            if 'alexnet' in label:
                l = int(label[-1])
                timeline_annotations = annotations['alexnet'][l]
            else:
                timeline_annotations = annotations[label]
            matrix_all[l_idx,:] = timeline_annotations

    # Plot
    mask_ROIs = np.zeros_like(matrix_all)
    mask_ROIs[l_idx_ROIs,:] = 1
    mask_ROIs = mask_ROIs.astype(bool)
    plt.figure(figsize=(12, 4))
    data_labels = np.ma.masked_array(matrix_all, mask = mask_ROIs) 
    data_ROIs = np.ma.masked_array(matrix_all, mask = np.invert(mask_ROIs))
    plt.imshow(data_labels, interpolation='none', aspect='auto', cmap='Blues', vmin=0)
    plt.imshow(data_ROIs, interpolation='none', aspect='auto', cmap='Greens', vmin=0)
    ylabels = []
    for label in labels:
        if 'alexnet' in label:
            ylabels.append('Alexnet L' + str(label[-1]))
        elif label in cfg.label_to_title.keys():
            ylabels.append(cfg.label_to_title[label])
        else:
            ylabels.append(ROI_label_to_ylabel[label])

    plt.yticks(range(len(ylabels)), ylabels)
    plt.xlabel('Timepoint')

    # Add horizontal lines
    ax = plt.gca()
    ax.set_yticks(np.arange(0.5, len(ylabels), 1), minor=True)
    plt.grid(which='minor', linewidth=1)
    ax.tick_params(which='minor', left = False)

    # Colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.1)
    plt.colorbar(cax=cax)

    plt.tight_layout()

    plt.savefig(save_dir + 'timeline_annotations_and_states_run' + str(run_nr) + '.pdf', bbox_inches='tight')
    plt.savefig(save_dir + 'timeline_annotations_and_states_run' + str(run_nr) + '.png', bbox_inches='tight')
    plt.savefig(save_dir + 'timeline_annotations_and_states_run' + str(run_nr) + '.svg', bbox_inches='tight')

# Values below can be adjusted to get a different run or annotation
labels = ['location2', 'location3', 'PPA_L', 'PPA_R']
run_nr = 2 

plot_timelines(labels, run_nr)