from mpl_toolkits.axes_grid1 import make_axes_locatable

from support.annotations import *
from support.funcs import *

import sys
sys.path.append("../..")

save_dir = cfg.dir_fig + 'annotations/'

def plot_timelines(labels, run_nr):

    # Get and plot annotations
    matrix_all = np.zeros((len(labels), cfg.nTRs[run_nr])) * np.nan
    annotations = Annotations(run_nr, delay_s = cfg.delay).get_changes_overTime()
    for l_idx, label in enumerate(labels):
        if 'alexnet' in label:
            l = int(label[-1])
            timeline_annotations = annotations['alexnet'][l]
        else:
            timeline_annotations = annotations[label]
        matrix_all[l_idx,:] = timeline_annotations

    # Plot
    plt.figure(figsize=(12, 4))
    plt.imshow(matrix_all, interpolation='none', aspect='auto', cmap='Blues', vmin=0)
    ylabels = []
    for label in labels:
        if 'alexnet' in label:
            ylabels.append('Alexnet L' + str(label[-1]))
        else:
            ylabels.append(cfg.label_to_title[label])
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

    plt.savefig(save_dir + 'timeline_annotations_run' + str(run_nr) + '.pdf', bbox_inches='tight')
    plt.savefig(save_dir + 'timeline_annotations_run' + str(run_nr) + '.png', bbox_inches='tight')
    plt.savefig(save_dir + 'timeline_annotations_run' + str(run_nr) + '.svg', bbox_inches='tight')


labels = ['event', 'location2', 'location3', 'shot', 'normdiff', 'alexnet7', 'alexnet6', 'alexnet5', 'alexnet4', 'alexnet3', 'alexnet2', 'alexnet1', 'alexnet0', 'speech', 'mfcc']
run_nr = 2
plot_timelines(labels, run_nr)