import warnings
import numpy as np
import random
import config as cfg
from matplotlib import pyplot as plt
from tqdm import tqdm

def permutation_test(strength_timeline, func_statistic, savename, show_progress=False, *arg):
    # Perform a permutation test with each permutation having a different order of states, but with the states still being of the same length
    # strength_timeline: vector with strength values per timepoint, with 0 denoting the absence of a boundary.
    # Importantly, this timeline is not (yet) convolved.
    # func_statistic: function to compute the statistic
    # *arg: any argument that has to be given to func_statitic, on top of strength_timeline

    stat_data = func_statistic(strength_timeline, *arg)
    num_perms = cfg.nr_permutations
    stat_null = np.ones((num_perms, len(stat_data)))

    if show_progress:
        for iteration in tqdm(range(num_perms)):
            strength_shuffled = shuffle_states(strength_timeline)
            stat_null[iteration,:] = func_statistic(strength_shuffled, *arg)
    else:
        for iteration in range(num_perms):
            strength_shuffled = shuffle_states(strength_timeline)
            stat_null[iteration, :] = func_statistic(strength_shuffled, *arg)

    if len(stat_data) > 1:
        # Get p value for each measure
        ps = []
        f, ax = plt.subplots(stat_null.shape[1], 1, figsize=(10, 20))
        for s_idx, s in enumerate(stat_data):
            p = np.sum(stat_null[:,s_idx] >= s)/num_perms # PLEASE DONT TOUCH THE >=! IT IS GOOD!
            ps.append(p)

            ax[s_idx].hist(stat_null[:, s_idx], bins = int(num_perms/10))
            ax[s_idx].axvline(stat_data[s_idx], c='k')
            plt.tight_layout()
        plt.savefig(savename)
        plt.close()
    else:
        ps = np.sum(stat_null >= stat_data)/num_perms
        plt.figure()
        try:
            plt.hist(stat_null, bins = int(num_perms/10))
            plt.axvline(stat_data, c='k')
        except:
            warnings.warn("Only Nans present in nulldistribution. The strength timeline probably only consists of zeros.")
        plt.savefig(savename)
        plt.close()

    mean_of_null = np.mean(stat_null, axis = 0)

    return ps, mean_of_null

def shuffle_states_run(timeline):
    # Get new order of state lengths
    state_order = np.arange(0, np.sum(timeline > 0) + 1)
    random.shuffle(state_order)

    # Get original start indices of each state
    state_start_org = np.where(timeline > 0)[0]
    state_start_org = np.insert(state_start_org, 0, 0)

    # Get strengths and re-order them
    strengths_shuffled = timeline[timeline>0]
    random.shuffle(strengths_shuffled)

    timeline_shuffled = []
    for strength_idx, state_idx in enumerate(state_order):
        # find start and end idx over time
        start = state_start_org[state_idx]
        if state_idx == np.max(state_order):
            end = len(timeline)
        else:
            end = state_start_org[state_idx + 1]
        state_length = end-start

        # If this is not the first state in the timeline, add the next strength
        if strength_idx is not 0:
            timeline_shuffled.append(strengths_shuffled[strength_idx-1])

            # Add the length to shuffled timeline
            timeline_shuffled.extend(np.zeros(state_length -1))
        else: # Add length without any strength
            timeline_shuffled.extend(np.zeros(state_length))

    return np.array(timeline_shuffled)

def shuffle_states(timeline):
    timeline_shuffled = timeline.copy()
    if type(timeline) is dict: # Shuffle within runs
        for run_nr in timeline.keys():
            timeline_shuffled[run_nr] = shuffle_states_run(timeline[run_nr])
    else:
        timeline_shuffled = shuffle_states_run(timeline)
    return timeline_shuffled


def p_to_arterisks(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"

def Bonferroni_for_ROIs(ps):
    ROIs = cfg.ROIs
    m = len(ROIs)
    significant_labels_dict = dict((ROI, []) for ROI in ROIs)

    # Go through ROIs and analyses
    for ROI in ROIs:
        for analysis_label in ps[ROI].keys():
            p = ps[ROI][analysis_label]
            if p < 0.05/m:
                significant_labels_dict[ROI].append(analysis_label)


    # Return
    return significant_labels_dict


def BH_correction_Sls(p_values, SL_indices):
    m = len(p_values)
    Q = 0.05

    BH_values = []
    ps_sorted = np.sort(p_values)
    SL_indices_sorted = np.asarray(SL_indices)[np.argsort(p_values)]

    # Compute BH values
    for rank_idx, label in enumerate(SL_indices_sorted):
        rank = rank_idx + 1
        BH_values.append((rank / m) * Q)

    # Get idx of highest p_value that is smaller than its BH_value
    comparisons = ps_sorted < np.array(BH_values)
    if np.sum(comparisons) > 0:
        idx_sign_end = np.where(comparisons)[0][-1]
        significant_labels = SL_indices_sorted[:idx_sign_end + 1]
        highest_p = ps_sorted[idx_sign_end]
    else: # Nothing is significant after correction
        significant_labels = []
        highest_p = np.nan
    return significant_labels, highest_p