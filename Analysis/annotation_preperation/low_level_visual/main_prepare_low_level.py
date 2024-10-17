import numpy as np
import config as cfg
import matplotlib.pyplot as plt
import csv

fps = 25
save_dir = cfg.dir_fig + 'low_level/'

def downsample(timeline):
    # To downsample, take the maximum difference per TR
    samples_per_interval = cfg.TR * fps

    timeline_ds = []
    for idx_start in range(0, len(timeline),samples_per_interval):
        interval = timeline[idx_start:idx_start+samples_per_interval]
        timeline_ds.append(np.max(interval))

    return np.asarray(timeline_ds)

for run_nr in range(1,9):
    # Get original annotation information
    # Run number starts at 1, segment number starts at 0
    filename = cfg.dir_annotations + 'visual/' + 'fg_av_ger_seg' + str(run_nr - 1) + '_normdiff.tsv'

    # Load information and store
    differences_normdiff = []
    with open(filename) as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for row_idx, row in enumerate(reader):
            differences_normdiff.append(float(row["norm_diff"]))
        tsv_file.close()

    # Save normdiff per frame as numpy
    np.save("run" + str(run_nr) + "_normdiff", differences_normdiff)

    # Load normdiff per frame information
    timeline = np.load('run' + str(run_nr) + '_normdiff.npy')

    # Downsample
    timeline_ds = downsample(timeline)

    # Add delay
    # ASSUMPTION: mod(delay,TR) is 0. Otherwise, delay has to be added before downsampling
    nr_extra_timepoints = int(cfg.delay_seconds / cfg.TR)
    inserted_value = np.mean(timeline_ds)
    timeline_ds = np.insert(timeline_ds, 0, np.ones(nr_extra_timepoints) * inserted_value)

    # Save
    np.save('run' + str(run_nr) + '_normdiff_downsampled', timeline_ds)

    # Plot
    plt.figure()
    plt.plot(timeline_ds)
    plt.savefig(save_dir + 'timeline run' + str(run_nr) + '_downsampled')