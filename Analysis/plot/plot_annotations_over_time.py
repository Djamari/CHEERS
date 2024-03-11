from support.annotations import *
from support.funcs import *
import config as cfg

save_dir = cfg.dir_fig + 'annotations/'

labels = ['event', 'location2', 'location3', 'shot', 'normdiff', 'alexnet']
labels_plot = labels[:-1]
labels_plot.extend(["L" + str(i) for i in range(cfg.nr_of_layers)])

# One figure per run
for run_nr in cfg.run_numbers:
    matrix = np.zeros((len(labels_plot), cfg.nTRs[run_nr]))
    A = Annotations(run_nr, delay_s=cfg.delay).get_changes_overTime()
    for label_idx, label in enumerate(labels):
        if label == 'alexnet':
            matrix[label_idx:label_idx+7] = A[label]
        else:
            matrix[label_idx, :] = A[label]

    plt.figure(figsize=(30, 10))
    plt.imshow(matrix, aspect='auto', cmap='PiYG', vmin=-1, vmax=1)
    # plt.xticks(np.arange(-0.5, timeline.shape[1]), [])
    plt.xlabel('Time (TR)', fontsize='xx-large')
    plt.title("Run " + str(run_nr))
    plt.yticks(np.arange(0,len(labels_plot)), labels_plot, fontsize=24)
    plt.tight_layout()
    plt.savefig(save_dir + "all_labels_run" + str(run_nr))



