import seaborn as sns
from support.annotations import *
from support.funcs import *
from plot_match_per_ROI import ROI_to_text

sns.set()
dir_save = cfg.dir_fig + 'Analysis results/extra/'
run_nr = 4
delays = np.arange(0, 10, 0.5)

ROI_names = []
for ROI in cfg.ROIs:
    if "L" in ROI:
        name = "Left "
    else:
        name = "Right "
    name += ROI_to_text(ROI)
    ROI_names.append(name)

def Jaccard(vector1, vector2):
    comb = vector1 + vector2
    return np.sum(comb > 1) / np.sum(comb > 0)


overlaps = np.zeros_like(delays)
f, ax = plt.subplots(2, 2, figsize=(9, 6))
alpha = ['A) ', 'B) ', 'C) ']
for ROI_index, ROI in enumerate(cfg.ROIs):
    for d_idx, d in enumerate(delays):
        # Get events
        events = Annotations(run_nr=run_nr, delay_s=d).get_changes_overTime('event')

        # Load a GSBS object
        filename = '/home/djaoet/wrkgrp/Djamari/StudyForrest/GSBS results/ROIs/' + 'GSBS_run' + str(
            run_nr) + '_finetune' + str(cfg.finetune) + '_' + ROI + '.npy'
        GSBS_results = np.load(filename, allow_pickle=True).item()
        deltas = GSBS_results.get_deltas()

        # Compute overlap
        J = Jaccard(events, deltas)
        overlaps[d_idx] = J

    max_J = np.max(overlaps)
    best_delay = delays[np.argwhere(overlaps >= max_J - 0.001)]

    print(ROI + ": " + str(best_delay.flatten()))
    print(ROI + ": " + str(np.median(best_delay)))

    ax[np.unravel_index(int(ROI_index / 2), [2,2])].plot(delays, overlaps, color=cfg.ROI_colors[ROI], label=ROI_names[ROI_index])
    ax[1,1].scatter(best_delay, np.ones(len(best_delay)) * ROI_index, color=cfg.ROI_colors[ROI], zorder = 1+ROI_index)
    ax[np.unravel_index(int(ROI_index / 2), [2,2])].set_title(alpha[int(ROI_index/2)] + "Overlap in " + ROI_to_text(ROI), loc='left')

for i in range(3):
    plt.sca(ax[np.unravel_index(i, [2,2])])

    plt.legend()
    if i == 2:
        plt.xlabel('Delay (s)')
    plt.ylabel('Jaccard index')
    plt.ylim(ax[np.unravel_index(i, [2,2])].get_ylim())
    plt.vlines(x=cfg.delay, ymin=-1, ymax=0.15, linestyles='--', linewidth=0.8, color='black', zorder=1)
    plt.xticks(np.arange(0, 10), np.arange(0, 10))


plt.sca(ax[1,1])
plt.vlines(x=cfg.delay, ymin=-1, ymax=len(cfg.ROIs) + 5, linestyles='--', linewidth=0.8, color='black', zorder=1)
plt.ylim([-0.25,len(cfg.ROIs)-0.75])
plt.title("D) Optimal delays per ROI", loc='left')
plt.xlabel("Delay (s)")
plt.xlim([0, 10])
plt.xticks(np.arange(0, 10), np.arange(0, 10))
plt.yticks(np.arange(0, len(cfg.ROIs)), ROI_names)
plt.tight_layout()
plt.savefig(dir_save + 'Jaccard_over_delay.png')
plt.savefig(dir_save + 'Jaccard_over_delay.svg')
plt.savefig(dir_save + 'Jaccard_over_delay.eps')
plt.savefig(dir_save + 'Jaccard_over_delay.pdf')




