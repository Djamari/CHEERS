from support.annotations import *
from support.funcs import *
from scipy.stats import pearsonr

save_dir = cfg.dir_fig + 'Analysis results/extra/'
ROIs = cfg.ROIs

def get_full_timeline(timeline):
    timeline_all = []
    for run_nr in timeline.keys():
        timeline_all.extend(timeline[run_nr])
    return timeline_all

def get_full_timeline_annotations(annotations_perRun, label):
    timeline = []
    for run_nr in cfg.run_numbers:
        timeline.extend(annotations_perRun[run_nr][label])
    return timeline

def get_annotations_matrix(annotations, labels):
    annotation_matrix=[]
    # Per label, create full timeline and add to obs
    for idx, label in enumerate(labels):

        timeline_label = []
        for run_nr in cfg.run_numbers:
            timeline_label.extend(annotations[run_nr][label])

        # Add full timeline of label to observation matrix
        if idx == 0:
            annotation_matrix = timeline_label
        else:
            annotation_matrix = np.column_stack((annotation_matrix, timeline_label))

    # Add intersect
    annotation_matrix = np.column_stack((annotation_matrix, np.ones(annotation_matrix.shape[0])))
    return annotation_matrix

def get_annotation_matrix_sorted(annotations, labels):
    annotation_matrix=[]
    # Per label, create full timeline and add to obs
    for idx, label in enumerate(labels):

        timeline_label = []
        for run_nr in cfg.run_numbers:
            this_run = annotations[run_nr][label].copy()
            this_run.sort()
            timeline_label.extend(this_run)

        # Add full timeline of label to observation matrix
        if idx == 0:
            annotation_matrix = timeline_label
        else:
            annotation_matrix = np.column_stack((annotation_matrix, timeline_label))

    # Add intersect
    annotation_matrix = np.column_stack((annotation_matrix, np.ones(annotation_matrix.shape[0])))
    return annotation_matrix

def get_correlation(timeline_perRun, annotations_perRun):

    # Create full timeline
    timeline_all = np.asarray(get_full_timeline(timeline_perRun))

    Rs = []
    for label in cfg.analyses.keys():
        annotations = np.asarray(get_full_timeline_annotations(annotations_perRun, label))
        R, _ = pearsonr(timeline_all, annotations)
        Rs.append(R)
    return Rs


def get_max_correlation(timeline, annotations_per_run):
    max_Rs = []

    # Order timeline and concatenate
    timeline_ordered = []
    for run_nr in cfg.run_numbers:
        dummy = timeline[run_nr].copy()
        dummy.sort()
        timeline_ordered.extend(dummy)

    for label in cfg.analyses.keys():
        an_timeline = []
        for run_nr in cfg.run_numbers:
            an = annotations_per_run[run_nr][label].copy()
            an.sort()
            an_timeline.extend(an)

        max_R, _ = pearsonr(timeline_ordered,an_timeline)
        max_Rs.append(max_R)

    return max_Rs


def main_analysis():
    labels_this_analysis = list(cfg.analyses.keys())
    matches_ROIs_allRuns = dict((ROI, {}) for ROI in ROIs)
    matches_max_ROIs_allRuns = dict((ROI, {}) for ROI in ROIs)
    p_ROIs_allRuns = dict((ROI, {}) for ROI in ROIs)

    # Perform analysis per ROI
    for ROI_idx, ROI in enumerate(ROIs):
        print(ROI)

        strengths_all = dict((run_nr, []) for run_nr in cfg.run_numbers)
        annotations_all = dict((run_nr, []) for run_nr in cfg.run_numbers)
        for run_nr in cfg.run_numbers:
            # Get annotations
            annotations = Annotations(run_nr, delay_s=cfg.delay)
            annotations_overTime = annotations.get_changes_overTime(labels_this_analysis)

            # Load GSBS object
            filename = cfg.dir_GSBS_ROIs + 'GSBS_run' + str(run_nr) + '_finetune' + str(cfg.finetune) + '_' + ROI + '.npy'
            GSBS_results = np.load(filename, allow_pickle=True).item()

            strengths = GSBS_results.get_strengths()

            # Store
            strengths_all[run_nr] = strengths
            annotations_all[run_nr] = annotations_overTime

        # Get actual match
        match_data = get_correlation(strengths_all, annotations_all)

        # Permutation test
        savename = save_dir + 'trash/nulldistr_' + ROI + '_run'
        ps, match_null = permutation_test(strengths_all, get_correlation, savename, True, annotations_all)

        # Get maximum match possible
        match_max = get_max_correlation(strengths_all, annotations_all)

        # Store match and p value (as dictionary)
        for l, label in enumerate(labels_this_analysis):
            p_ROIs_allRuns[ROI][label] = ps[l]
            matches_ROIs_allRuns[ROI][label] = match_data[l]
            matches_max_ROIs_allRuns[ROI][label] = match_max[l]


    significant_labels_corrected = Bonferroni_for_ROIs(p_ROIs_allRuns)
    print(significant_labels_corrected)

    # Save results
    np.save(save_dir + "normal_correlation_ROIs_" + '_p_uncorrected', p_ROIs_allRuns)
    np.save(save_dir + "normal_correlation_ROIs_" + '_matches', matches_ROIs_allRuns)
    np.save(save_dir + "normal_correlation_ROIs_" + '_matches_max', matches_max_ROIs_allRuns)
    np.save(save_dir + "normal_correlation_ROIs_" + '_significant_labels_corrected',
            significant_labels_corrected)

if __name__ == '__main__':

    # Perform main analysis
    main_analysis()
