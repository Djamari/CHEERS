import config as cfg
import numpy as np
from os.path import exists

load_dir = cfg.dir_annotations + 'alexnet/'
distances = ['cosine', 'euclidean', 'R']
measure_over_spatial_dimension = [np.mean, np.max]

for measure in measure_over_spatial_dimension:
    for distance in distances:
        for run_nr in cfg.run_numbers:
            dir = load_dir + measure.__name__ + '_over_spatial/' + distance + '/'

            print("STARTING RUN " + str(run_nr))
            diffs_concatenated = dict((layer, [0]) for layer in range(8)) # add zero at the start for each run, to make it align to all other annotations
            for part in range(112):
                filename = "Alexnet_diffs_raw_run" + str(run_nr) + "_part" + str(part) + '.npy'


                if exists(dir + filename):
                    diffs = np.load(dir + filename, allow_pickle=True).item()
                    for layer in range(8):
                        diffs_concatenated[layer].extend(diffs[layer])

                else:
                    print("Does not exist: run " + str(run_nr) + ", part " + str(part))

            np.save(dir + "Alexnet_diffs_raw_run" + str(run_nr) + "_allframes", diffs_concatenated)