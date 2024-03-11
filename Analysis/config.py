### Analysis ###
ROIs = ['VIS_L', 'VIS_R','PPA_L', 'PPA_R','RSC_L', 'RSC_R']
delay = 4.5 # in seconds, based on Analysis/extra/main_HRD_delay.py
nr_permutations = 1000
alexnet_distance = 'cosine'
alexnet_spatialdimension_measure = 'mean'
finetune = 1
nr_of_layers = 8
labels_all = ["normdiff", "shot", "location2", "location3", "event"]
run_numbers = [1,2,3,5,6,7,8]

# Description of analysis: [label of interest]: [covariate1, covariate2, ...]
analyses = {
    'normdiff': ['location3', 'location2', 'event'],
    'location2': ['alexnet', 'normdiff', 'shot', 'event'],
    'location3': ['alexnet', 'normdiff', 'shot', 'event'],
    'event': ['alexnet', 'normdiff', 'shot', 'location3', 'location2'],
    'shot': ['alexnet', 'normdiff', 'location2', 'location3', 'event']
}

supplementary_analyses = ['shot']

# Searchlight parameters
SL_stride=2
SL_radius=3.5
SL_min_vox=20
kmax_ratio=0.5

### Colors for Plotting ###
pallet = {
    'blue dark': '#426194',
    'blue light': '#6B8ABD',
    'green dark': '#458354',
    'green light': '#73B583',
    'orange dark': '#CC662E',
    'orange light': '#DF9872'
}

colorblind_scheme={
    'black': '#000000',
    'orange': '#E69F00',
    'lightblue': '#56B4E9',
    'green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'red': '#D55E00',
    'purple': '#CC79A7',
    'brown': '#753E00'
}


ROI_colors = {
    'RSC_L': pallet['orange light'],
    'RSC_R': pallet['orange dark'],
    'PPA_L': pallet['green light'],
    'PPA_R': pallet['green dark'],
    'VIS_L': pallet['blue light'],
    'VIS_R': pallet['blue dark']
}


label_to_title = {
    'normdiff': 'Low-level visual features',
    'shot': 'Shots',
    'location3': 'Small-scale locations',
    'location2': 'Large-scale locations',
    'event': 'Events'
}

whole_brain_slices = {'normdiff':  [(-7, -89, 5), # EV
                    (-26,-54,-12)], # PPA
                      'location3': [(27, -40, -8), # PPA
                                    (-33,-88,8)],
                    'location2': [(27, -40, -8), # PPA
                                    (-33,-88,8)],# PPA
                      'event': [(-12, 54, 18), #
                                (-45,-60,-18)] #
                      }


background_image = "/home/djaoet/wrkgrp/Djamari/atlas/ch2better_whitebg.nii"


### Data info ###
TR = 2
fps = 25
nTRs = {
    1: 451,
    2: 441,
    3: 438,
    4: 488,
    5: 462,
    6: 439,
    7: 542,
    8: 338
}

count = 0
for run_nr in run_numbers:
    count += nTRs[run_nr]
nTRs_total = count

### Directories ###
dir_root = '[depending on user]/'
dir_preGSBS     = dir_root + 'preGSBS/'
dir_GSBS_ROIs   = dir_root + 'GSBS/ROIs/'
dir_GSBS_SLs    = dir_root + 'GSBS/searchlights/'
dir_fig         = dir_root + 'figures/'
dir_annotations = dir_root + 'stimulus/annotations/'
dir_p           = dir_root + 'p_values/'
dir_rawData     = dir_root + 'data raw/func/'
dir_movie       = dir_root + 'stimulus/'
dir_ROI         = dir_root + 'data raw/masks/ROIs/'
dir_normdiff    = '[retracted]/Analysis/annotation_preperation/low_level/'