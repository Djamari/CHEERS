import config as cfg
import numpy as np

load_dir = cfg.dir_annotations + 'alexnet/'
distance = cfg.alexnet_distance
measure = cfg.alexnet_spatialdimension_measure

def downsample(diffs, samples_per_interval):
    timeline_ds = np.zeros((len(diffs.keys()), cfg.nTRs[run_nr]))  # layer x TR
    for TR_idx, idx_start in enumerate(range(0, len(diffs[0]), samples_per_interval)):
        if not TR_idx == cfg.nTRs[run_nr]:  # The last couple of frames are not a full TR
            if TR_idx < cfg.nTRs[run_nr]:
                for layer_idx in range(len(diffs.keys())):
                    interval = diffs[layer_idx][idx_start:idx_start + samples_per_interval]
                    timeline_ds[layer_idx, TR_idx] = np.max(interval)

    return timeline_ds

for run_nr in cfg.run_numbers:
    # Load
    dir = load_dir + measure + '_over_spatial/' + distance + '/'
    diffs = np.load(dir + "Alexnet_diffs_raw_run" + str(run_nr) + "_allframes.npy", allow_pickle=True).item()

    # Add delay
    samples_added = int(cfg.fps * cfg.delay)  # skips one sample if delay is e.g. 5.5
    for l in diffs.keys():
        diffs[l] = np.concatenate((np.zeros(samples_added), diffs[l]))

    # Downsample
    diffs_ds = downsample(diffs, samples_per_interval=cfg.TR * cfg.fps)

    # Save whole run, including "downsampled" and "delay"
    np.save(cfg.dir_annotations + 'alexnet/downsampled/Alexnet_' + distance + '_' + measure + '_delay' + str(cfg.delay) + '_run' + str(run_nr) + '.npy', diffs_ds)