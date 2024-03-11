from Alexnet import Alexnet_rect
from PIL import Image
import numpy as np
from tqdm import tqdm
from mxnet import nd, gpu, Context, cpu
from scipy import spatial, stats
from os.path import exists
from enum import Enum
import config as cfg

class Device(Enum):
    CPU = -1
    GPU0 = 0
    GPU1 = 1
    GPU2 = 2

part_size = 250
device = Device.CPU


if device == Device.CPU:
    context = cpu()
else:
    context = gpu(device.value)

def get_diff(A, B, distance_name):
    if distance_name == 'cosine':
        return spatial.distance.cosine(A, B)
    if distance_name == 'euclidean':
        return np.linalg.norm(A-B)
    if distance_name == 'R':
        R, _ = stats.pearsonr(A,B)
        return 1 - R


distances = ['cosine', 'euclidean', 'R'] # though R would actually be 1-R to make it a distance
measure_over_spatial_dimension = [np.mean, np.max]

save_dir = cfg.dir_annotations + 'alexnet/'


def compute_alexnet_distances_allframes(run_nr, part):

        number_of_frames = {
            1: 22575,
            2: 22076,
            3: 21926,
            4: 24426,
            5: 23126,
            6: 21976,
            7: 27126,
            8: 16901,
        }
        frame_start = part * part_size + 1 # +1 because frame names start with 1

        if frame_start <= number_of_frames[run_nr]:
            frame_end = np.min((frame_start + part_size, number_of_frames[run_nr]))

            frame_dir = cfg.dir_movie + "frames native/Run" + str(run_nr) + "/"
            frame_numbers_this_part = np.arange(frame_start, frame_end)

            frames = []
            print("Loading frames: Run " + str(run_nr))
            for f in tqdm(frame_numbers_this_part):
                filename = frame_dir + 'frame' + str(f) + '.jpg'
                frame = Image.open(filename)
                frames.append(nd.array(frame))

            print("Preprocessing frames")

            frames_preprocessed = Alexnet_rect.preprocess(context, frames, downsample=False)

            # Loop through images, get output of model, compare to previous one, and store distance
            if part == 0:
                diffs = dict((measure,dict((d,dict((l,[0]) for l in range(8))) for d in distances)) for measure in measure_over_spatial_dimension)
            else:
                diffs = dict((measure,dict((d,dict((l,[]) for l in range(8))) for d in distances)) for measure in measure_over_spatial_dimension)

            for layer in range(8):
                if not exists(save_dir + "lastOutput_run" + str(run_nr) + "_part" + str(part) + "_layer" + str(layer) + ".np"):

                    print("Starting: Run " + str(run_nr) + ", Layer " + str(layer))
                    model = Alexnet_rect(context=context, layer=layer)

                    if part == 0:
                        output_previous = None
                    else:
                        # Load last output
                        output_previous = np.load(save_dir + "saved_outputs/lastOutput_run" + str(run_nr) + "_part" + str(part-1) + "_layer" + str(layer) + '.npy', allow_pickle=True)

                    # For loop because in one go takes too long or gives error
                    for frames_p in tqdm(frames_preprocessed):
                        output = model.hybrid_forward(context, frames_p).asnumpy()

                        for measure in measure_over_spatial_dimension:
                            # Get rid of spatial dimensions
                            output_1d = measure(measure(output, axis=-1), axis=-1).flatten()
                            if output_previous is not None:
                                output_previous_1d = measure(measure(output_previous, axis=-1), axis=-1).flatten()

                            # Compare to previous
                            for distance in distances:
                                if output_previous is not None:
                                    diff = get_diff(output_previous_1d,output_1d,distance)
                                    diffs[measure][distance][layer].append(diff)
                        output_previous = output
                    print("Done: Run " + str(run_nr) + ", Layer " + str(layer), ", Part " + str(part))
                    np.save(save_dir + "saved_outputs/lastOutput_run" + str(run_nr) + "_part" + str(part) + "_layer" + str(layer), output_previous)

            print("Saving distances")
            for measure in measure_over_spatial_dimension:
                m_name = measure.__name__
                for distance in distances:
                    dir = save_dir + m_name + '_over_spatial/' + distance + '/'
                    np.save(dir + "Alexnet_diffs_raw_run" + str(run_nr) + "_part" + str(part), diffs[measure][distance])


# Get alexnet distances per run in parts to lower computational load
for part in range(112): # 112 is a big enough number to ensure all runs are fully considered
    print("STARTING PART " + str(part))

    for run_nr in cfg.run_numbers:
        if device == Device.CPU:
            compute_alexnet_distances_allframes(run_nr, part)
        else:
            with Context(context):
                compute_alexnet_distances_allframes(run_nr, part)