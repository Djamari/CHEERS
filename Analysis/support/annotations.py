import config as cfg
import csv
import numpy as np
from scipy.spatial.distance import cosine
import librosa

class Annotations:

    def __init__(self, run_nr, delay_s, load_audio=True):
        self.run_nr = run_nr
        self.delay_s = delay_s

        filename_an = cfg.dir_annotations + 'locations_run-' + str(run_nr) + '_events.tsv'
        filename_events = cfg.dir_annotations + 'events run' + str(self.run_nr) + '.tsv'
        filename_alexnet = cfg.dir_annotations + 'alexnet/downsampled/Alexnet_' + cfg.alexnet_distance + '_' + cfg.alexnet_spatialdimension_measure + '_delay' + str(cfg.delay) + '_run' + str(run_nr) + '.npy'
        filename_speech = cfg.dir_annotations + 'audio/fg_rscut_ad_ger_speech_tagged.tsv'
        filename_audio = cfg.dir_root + 'stimulus/fg_av_seg' + str(run_nr - 1) + '.mp3'

        if delay_s is None:
            filename_normdiff = cfg.dir_normdiff + 'run' + str(run_nr) + '_normdiff_downsampled.npy'
        else:
            filename_normdiff = cfg.dir_normdiff + 'run' + str(run_nr) + '_normdiff.npy'
        self.nTRs = cfg.nTRs[run_nr]
        self.__read_tsv___(filename_an)
        self.__compute_changes__()
        self.__compute_changes_overTime__()
        self.__add_events__(filename_events)
        self.__add_normdiff__(filename_normdiff)
        self.__add_speech_annotations__(filename_speech)
        if load_audio:
            self.__add_mfcc(filename_audio)
            
        if run_nr != 4: # Alexnet distances does not exist for run 4
            self.__add_alexnet__(filename_alexnet)

    ### Private functions ###
    def __read_tsv___(self, filename_an):
        self.__raw__ = {
            "time": [],
            "duration": [],
            "location1": [],
            "location2": [],
            "location3": [],
            "interior": [],
            "jump": [],
            "daytime": [],
        }
        with open(filename_an) as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter='\t')
            for row in reader:
                # Add timing as double
                self.__raw__["time"].append(float(row["onset"]))

                # Add duration as double
                self.__raw__["duration"].append(float(row["duration"]))

                # Add location1 (major location) as string
                self.__raw__["location1"].append(row["major_location"])

                # Add location2 (setting) as string
                self.__raw__["location2"].append(row["setting"])

                # Add location3 (major location) as string
                self.__raw__["location3"].append(row["locale"])

                # Interior (true) or exterior (false) as boolean
                self.__raw__["interior"].append(row["int_or_ext"] == "int")

                # Add time jump as int (-1, 0, 1, 2)
                if row["flow_of_time"] == "-":
                    self.__raw__["jump"].append(-1)
                elif row["flow_of_time"] == "0":
                    self.__raw__["jump"].append(0)
                elif row["flow_of_time"] == "+":
                    self.__raw__["jump"].append(1)
                elif row["flow_of_time"] == "++":
                    self.__raw__["jump"].append(2)
                else:
                    print(row)

                # Add time of day as boolean (true = day, false = night)
                self.__raw__["daytime"].append(row["time_of_day"] == "day")

            tsv_file.close()

    def __compute_changes__(self):
        changes = {
            "location1": [False],
            "location2": [False],
            "location3": [False],
            "interior": [False],
            "jump": [False],
            "daytime": [False],
            "event": [],
            "normdiff": []
        }

        # Original annotations
        for i in range(1, len(self.__raw__["location1"])):
            loc1_old = self.__raw__["location1"][i-1]
            loc1_new = self.__raw__["location1"][i]
            changes["location1"].append(loc1_old != loc1_new)

            loc2_old = self.__raw__["location2"][i-1]
            loc2_new = self.__raw__["location2"][i]
            changes["location2"].append(loc2_old != loc2_new)

            loc3_old = self.__raw__["location3"][i-1]
            loc3_new = self.__raw__["location3"][i]
            changes["location3"].append(loc3_old != loc3_new)

            int_old = self.__raw__["interior"][i-1]
            int_new = self.__raw__["interior"][i]
            changes["interior"].append(int_old != int_new)

            daytime_old = self.__raw__["daytime"][i-1]
            daytime_new = self.__raw__["daytime"][i]
            changes["daytime"].append(daytime_old != daytime_new)

            changes["jump"].append(self.__raw__["jump"][i] != 0)

        self.__changes__ = changes

    def __compute_changes_overTime__(self):

        timepoints_changes = {}
        timepoints_all = np.asarray(self.__raw__['time'])
        for label in cfg.labels_all:
            if label == 'shot':
                timepoints_changes[label] = timepoints_all
            else:
                timepoints_changes[label] = timepoints_all[self.__changes__[label]]


        # Convert to time axis
        self.__changes_overTime_downsampled__ = {}
        TR = cfg.TR
        for key in timepoints_changes.keys():
            # Add delay
            if self.delay_s is not None:
                timepoints_changes[key] += self.delay_s

            pre_ds = np.asarray(timepoints_changes[key])
            indices = (pre_ds / TR).astype(int)

            post_ds = np.zeros(self.nTRs)
            post_ds[indices] = 1

            # No change at first volume
            post_ds[0] = 0.0

            self.__changes_overTime_downsampled__[key] = post_ds

    def __add_events__(self, filename_events):
        # Events
        event_timings = []
        with open(filename_events) as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter='\t')
            for row in reader:
                # Add timing as double
                event_timings.append(float(row["time"]))
            tsv_file.close()
        event_timings = np.asarray(event_timings)

        # add delay
        if self.delay_s is not None:
            event_timings += self.delay_s

        indices = (event_timings / cfg.TR).astype(int)

        post_ds = np.zeros(self.nTRs)
        post_ds[indices] = 1

        self.__changes_overTime_downsampled__['event'] = post_ds

    def __add_normdiff__(self, filename_normdiff):

        # Load
        timeline = np.load(filename_normdiff)
        timeline = np.delete(timeline, 0) # Removing first frame because normdiff file was 1 frame off wrt shots/locations file


        samples_per_interval = cfg.TR * cfg.fps
        samples_added = int(cfg.fps * self.delay_s) # skips one sample if delay is e.g. 5.5

        # add delay
        timeline = np.concatenate((np.zeros(samples_added), timeline))

        # Downsample
        timeline_ds = []
        for idx_start in range(0, len(timeline), samples_per_interval):
            interval = timeline[idx_start:idx_start + samples_per_interval]
            timeline_ds.append(np.max(interval))
        timeline = timeline_ds

        # Cut the end until number of TRs is correct
        len_diff = len(timeline) - self.nTRs
        timeline = timeline[: -1 * len_diff]

        self.__changes_overTime_downsampled__['normdiff'] = timeline

    def __add_alexnet__(self, filename_alexnet):
        # Load alexnet distances
        alexnet_distances = np.load(filename_alexnet, allow_pickle=True)

        # Scale
        for layer in range(alexnet_distances.shape[0]):
            alexnet_distances[layer] /= np.max(alexnet_distances[layer])

        # Store, but only take the first X layers,
        self.__changes_overTime_downsampled__['alexnet'] = alexnet_distances[:cfg.nr_of_layers,:]


    def __add_speech_annotations__(self, filename_speech):
        t_run_start = cfg.speech_annotations_start_run[self.run_nr]
        if self.run_nr == 8:
            t_run_end = 9999.99
        else:
            t_run_end = cfg.speech_annotations_start_run[self.run_nr + 1]

        # Get per timepoint whether a word as being spoken or not
        words_onset = []
        words_offset = []
        with open(filename_speech) as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter='\t')
            for row in reader:
                # Get the global timing from the annotation file
                timing_global = float(row['onset'])

                # Continue if timing is not part of this run
                if timing_global < t_run_start or timing_global >= t_run_end:
                    continue

                # Compute the run-specific timing
                timing_run = timing_global - t_run_start

                # Get speaker info
                speaker = row['person']

                # If not the narrator and if available, this is a timepoint with a word
                if len(row['vector']) > 0 and speaker != 'NARRATOR':
                    # Store the onset
                    words_onset.append(timing_run)
                    # Store the offset
                    words_offset.append(round(timing_run + float(row['duration']), 3))

            tsv_file.close()

        # Get vector of 'speech or not' per timepoint
        speech = np.zeros(self.nTRs * cfg.TR * 1000) # 1000 values per second, as in annotation file
        for word_idx in range(len(words_onset)):
            t_idx_start = int(words_onset[word_idx] * 1000)
            t_idx_end = int(words_offset[word_idx] * 1000)
            speech[t_idx_start:t_idx_end] = 1

        # Fill zeros with ones if the duration of no speech is less than one TR
        t_idx_start = 0
        while t_idx_start  < len(speech):
            if speech[t_idx_start] == 0:
                t_idx_end = t_idx_start
                # Get number of zeros after this until the next 1
                while t_idx_end < len(speech) and speech[t_idx_end] == 0:
                    t_idx_end += 1
                duration = (t_idx_end - t_idx_start)/1000
                if duration <= cfg.TR:
                    speech[t_idx_start:t_idx_end] = 1

                # Update t_idx
                t_idx_start = t_idx_end
            else:
                t_idx_start += 1

        # Convert to change in speech
        speech_change = np.zeros_like(speech)
        for t_idx in range(1,len(speech)):
            if speech[t_idx] != speech[t_idx-1]:
                speech_change[t_idx] = 1

        # Add delay
        speech_change = np.concatenate((np.zeros(int(self.delay_s * 1000)), speech_change))

        # Downsample
        speech_timeline = []
        for t_idx in range(0,len(speech), cfg.TR * 1000):
            if np.sum(speech_change[t_idx:t_idx + cfg.TR*1000]) > 0:
                speech_timeline.append(1)
            else:
                speech_timeline.append(0)
        speech_timeline = np.asarray(speech_timeline)

        # Store
        self.__changes_overTime_downsampled__['speech'] = speech_timeline

    def __add_mfcc(self, audiofile):
        # Load audio file and information
        audio = librosa.load(audiofile, sr=None, mono=True)[0]
        sr = librosa.get_samplerate(audiofile)
        audio_duration = audio.shape[0] / sr  # in seconds

        # Get MFCC and sr of MFCC
        mfcc_timeline = librosa.feature.mfcc(audio,hop_length=525)
        sr_MFCC = mfcc_timeline.shape[1] / audio_duration


        # Add delay
        samples_to_add = int(self.delay_s * sr_MFCC)
        mfcc_timeline_delayed = np.concatenate((np.zeros((mfcc_timeline.shape[0],samples_to_add)), mfcc_timeline), axis=1)

        # Downsample
        samples_per_interval = int(sr_MFCC * cfg.TR)
        timeline_ds = np.zeros((mfcc_timeline_delayed.shape[0],cfg.nTRs[self.run_nr]))
        for TR_idx, idx_start in enumerate(range(0, mfcc_timeline_delayed.shape[1], samples_per_interval)):
            if TR_idx < cfg.nTRs[self.run_nr]:
                interval = mfcc_timeline_delayed[:, idx_start:idx_start + samples_per_interval]
                timeline_ds[:,TR_idx] = np.mean(interval, axis=1)

        # Compute cosine difference per TR
        diffs = [0]
        for t in range(1, timeline_ds.shape[1]):
            frame1 = timeline_ds[:, t - 1]
            frame2 = timeline_ds[:, t]
            diffs.append(cosine(frame1, frame2))
        diffs = np.asarray(diffs)

        # Store info (and scale)
        self.__changes_overTime_downsampled__['mfcc'] = diffs / np.max(diffs)

    ### Getters ###
    def get_rawAnnotations(self, key=None):
        if key is None:
            return self.__raw__
        else:
            return self.__raw__[key]


    def get_changes_overTime(self, key=None):
        ans = self.__changes_overTime_downsampled__.copy()
        if key is None:
            return ans
        else:
            if type(key) == list:
                to_return = {}
                for label in key:
                    to_return[label] = ans[label]
                return to_return
            else:
                return ans[key]


