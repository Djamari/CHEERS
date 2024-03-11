##################################################
# Contains regularly used functions for plotting #
##################################################
import config as cfg
import matplotlib.patches as patches
import numpy as np

def time_correlation_simple(ax, GSBS=None, threshold = False):
    # ax: where it is plotted
    # data: 2D matrix, time x voxels
    # GSBS (opt): GSBS object

    # Compute corrcoef
    data = GSBS.x
    corr = np.corrcoef(data)

    # Plot the matrix
    ax.imshow(corr, interpolation='none')
    ax.set_xlabel('TR')
    ax.set_ylabel('TR')

    # Plot the boundaries
    if GSBS is not None:
        strengths = GSBS.get_strengths()
        if threshold:
            strengths[strengths < cfg.strength_threshold] = 0
        bounds = np.where(strengths > 0)[0]

        for i in range(len(bounds)-1):
            rect = patches.Rectangle(
                (bounds[i], bounds[i]),
                bounds[i + 1] - bounds[i],
                bounds[i + 1] - bounds[i],
                linewidth=2, edgecolor='r', facecolor='none'
            )
            ax.add_patch(rect)

def tdistance_over_states(ax, GSBS, ROI=None):
    if ROI is None:
        ax.plot(GSBS.tdists, label=ROI)
        ax.plot(GSBS.nstates, GSBS.tdists[GSBS.nstates], 'ro')
    else:
        ax.plot(GSBS.tdists, label=ROI, color=cfg.ROI_colors[ROI])
        ax.scatter(GSBS.nstates, GSBS.tdists[GSBS.nstates], marker='o', color=cfg.ROI_colors[ROI], edgecolors='k')
    ax.set_xlabel('Number of states')
    ax.set_ylabel('T-distance')

