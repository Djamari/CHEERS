from mvpa2.suite import *
import time

# Use one run to estimate parameters
run_nr = 4

# Directories
datadir = '[redacted]/StudyForrest/data raw/func/'
maskdir =  '[redacted]/StudyForrest/data raw/masks/'
saved_variables_dir = 'saved_variables/'

# Function to compute the reference subject based on ISS
def compute_ISS(run_datasets,nTime):
    subsim = np.empty((len(run_datasets), len(run_datasets)))
    for i in range(len(run_datasets)):
        for j in range(i, len(run_datasets)):
            subsim[i, j] = np.mean(nTime * np.mean(np.multiply(run_datasets[i], run_datasets[j]), 0)/(nTime-1))
            subsim[j, i] = subsim[i, j]
    refsub = np.argmax(np.mean(subsim, 0))
    return refsub

# Get list of subjects
allfiles = os.listdir(datadir)
namelist=[]
for names in allfiles:
    if names.startswith("sub") and not names.endswith("phantom"):
        namelist.append(names)
namelist.sort()

# Load gray matter mask
maskdir = maskdir + 'GM_mask.nii'
mask = fmri_dataset(samples=maskdir, mask=maskdir)
mask = np.where(mask.samples>0)[1]

# Load all the data for the searchlight hyperalignment
run_datasets = []
for count, name in enumerate(namelist):
    print(count/len(namelist)*100)
    print("Loading " + name)

    filename = datadir + name + '/ses-movie/func/waligned_' + name + '_ses-movie_task-movie_run-' + str(run_nr) + '_space-T1w_desc-unsmDenoised_bold.nii'
    alldata = fmri_dataset(samples=filename, mask=maskdir)

    nTimePoints = alldata.samples.shape[0]

    alldata.sa._uniform_length = nTimePoints
    alldata.sa['time_indices'] = range(nTimePoints)
    alldata.sa['time_coords'] = np.zeros(nTimePoints)
    zscore(alldata, chunks_attr=None, param_est=None)
    run_datasets.append(alldata)

# Get reference subject
refsub = compute_ISS(run_datasets, nTimePoints)
refsub_name = namelist[refsub]
print("Reference subject: " + refsub_name)

# Settings for hyperalignment
hyper = Hyperalignment(level1_equal_weight=True)

# Settings for SL hyperalignment
slhyper = SearchlightHyperalignment(radius=3, ref_ds=refsub, nblocks=50, compute_recon=False, hyperalignment=hyper, mask_node_ids=mask)

# Compute hyperalignment parameters
print("Computing hyperalignment parameters")
start_time = time.time()
slhypmaps = slhyper(run_datasets)
end_time = time.time()
print("Done")
print("Computation time: %s seconds" % (end_time - start_time))


# Apply hypperalignment parameters on all data
for count, name in enumerate(namelist):
    print(count / len(namelist) * 100)
    for run in range(1,9):
        filename = datadir + name + '/ses-movie/func/waligned_' + name + '_ses-movie_task-movie_run-' + str(run) + '_space-T1w_desc-unsmDenoised_bold.nii'
        data_run = fmri_dataset(samples=filename, mask=maskdir)

        nTimePoints = data_run.samples.shape[0]
        data_run.sa._uniform_length = nTimePoints
        data_run.sa['time_indices'] = range(nTimePoints)
        data_run.sa['time_coords'] = np.zeros(nTimePoints)
        zscore(data_run, chunks_attr=None, param_est=None)

        # Apply parameters
        print("Applying parameters on " + name + " run " + str(run))
        data_run_hyper = slhypmaps[count].forward(data_run)

        # Save hyperaligned data
        print("Saving hyperaligned data " + name + " run " + str(run))
        img = map2nifti(data_run_hyper)
        save(img, datadir + name + '/ses-movie/func/' + name + '_movie_run-' + str(run) + '_hyperaligned.nii')