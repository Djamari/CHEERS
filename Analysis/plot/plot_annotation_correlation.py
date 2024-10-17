import numpy as np
import matplotlib.pyplot as plt
import config as cfg
from support.annotations import Annotations
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import stats
import seaborn as sns

sns.set()

save_dir = cfg.dir_fig + 'annotations/'

labels_all =  ['event', 'location2', 'location3', 'shot', 'normdiff', 'alexnet7', 'alexnet6', 'alexnet5', 'alexnet4', 'alexnet3', 'alexnet2', 'alexnet1', 'alexnet0', 'speech', 'mfcc']
# Get all annotations together
annotations_all = dict((label,[]) for label in labels_all)
for run_nr in cfg.run_numbers:
    annotations_run = Annotations(run_nr,delay_s=cfg.delay).get_changes_overTime()
    for label in labels_all:
        if 'alexnet' in label:
            l = int(label[-1])
            annotations_all[label].extend(annotations_run['alexnet'][l,:])
        else:
            annotations_all[label].extend(annotations_run[label])

Rs = np.zeros((len(labels_all), len(labels_all)))
for idx1, l1 in enumerate(labels_all):
    for idx2, l2 in enumerate(labels_all):
        an1 = annotations_all[l1]
        an2 = annotations_all[l2]
        R, p = stats.pearsonr(an1, an2)
        Rs[idx1,idx2] = R

# Print some info
print("Average Rs:")
for l, label in enumerate(labels_all):
    print(label + ": " + str(np.mean(Rs[l,:])))


plt.figure(figsize=(7.5,7.5))
plt.imshow(Rs, vmin=0, vmax=1, interpolation='none', aspect='equal', cmap='summer')

labels_plot = []
for label in labels_all:
    if 'alexnet' in label:
        labels_plot.append('Alexnet L' + str(label[-1]))
    else:
        labels_plot.append(cfg.label_to_title[label])

plt.yticks(range(len(labels_plot)), labels_plot)
plt.xticks(range(len(labels_plot)), labels_plot, rotation='vertical')

# Set white lines around values
ax = plt.gca()
ax.grid(False)
ax.set_xticks(np.arange(-0.5,15,1),minor=True)
ax.set_yticks(np.arange(-0.5,15,1),minor=True)
ax.grid(which='minor', color='k',linestyle='-', linewidth=0.5)
ax.tick_params(which='minor', bottom=False, left=False)

# colorbar
divider = make_axes_locatable(ax)
cax=divider.append_axes("right", size="5%", pad=0.1)
plt.colorbar(cax=cax)

# Save
plt.tight_layout()
plt.savefig(save_dir + 'annotation_correlations.svg')
plt.savefig(save_dir + 'annotation_correlations.eps')
plt.savefig(save_dir + 'annotation_correlations.png')