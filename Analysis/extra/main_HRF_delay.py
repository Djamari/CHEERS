from support.annotations import *
from support.funcs import *

dir_save = cfg.dir_fig + 'delay/'
run_nr = 4
delays = np.arange(0,10,0.5)

def Jaccard(vector1, vector2):
    # Jaccard index: how often do both vectors have a 1?
    comb = vector1 + vector2
    return np.sum(comb>1)/np.sum(comb>0)

overlaps = np.zeros_like(delays)
f, ax = plt.subplots(4,1, figsize=(5,10))

# Loop through ROIs and possible delays
for ROI_index, ROI in enumerate(cfg.ROIs):
    for d_idx, d in enumerate(delays):
        # Get events
        events = Annotations(run_nr=run_nr, delay_s=d).get_changes_overTime('event')

        # Load a GSBS object
        filename = '/home/djaoet/wrkgrp/Djamari/StudyForrest/GSBS results/ROIs/' + 'GSBS_run' + str(run_nr) + '_finetune' + str(cfg.finetune) + '_' + ROI + '.npy'
        GSBS_results = np.load(filename, allow_pickle=True).item()
        deltas = GSBS_results.get_deltas()

        # Compute overlap
        J = Jaccard(events, deltas)
        overlaps[d_idx] = J

    # Compute optimal delay for this ROI
    max_J = np.max(overlaps)
    best_delay = delays[np.argwhere(overlaps >= max_J - 0.001)]
    
    print(ROI + ": " + str(best_delay.flatten()))
    print(ROI + ": " + str(np.median(best_delay)))
    ax[int(ROI_index/2)].plot(delays, overlaps, color=cfg.ROI_colors[ROI], label=ROI)
    ax[3].scatter(best_delay, np.ones(len(best_delay)) * ROI_index,color=cfg.ROI_colors[ROI])

# Finalize plot
for i in range(3):
    plt.sca(ax[i])
    plt.legend()
    plt.xlabel('Delay (s)')
    plt.ylabel('Jaccard index')
    plt.xticks(np.arange(0, 10), np.arange(0, 10))

plt.sca(ax[3])
plt.title("Optimal delays per ROI")
plt.xlabel("Delay (s)")
plt.xlim([0,10])
plt.xticks(np.arange(0,10),np.arange(0,10))
plt.yticks(np.arange(0,len(cfg.ROIs)), cfg.ROIs)
plt.tight_layout()
plt.savefig(dir_save + 'Jaccard_over_delay.png')
plt.savefig(dir_save + 'Jaccard_over_delay.svg')
plt.savefig(dir_save + 'Jaccard_over_delay.eps')




