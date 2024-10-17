%-----------------------------------------------------------------------
% Per subject, take the first volume of each run and align these volumes to
% each other.
% The data was already partially preprocessed, but the images were slightly
% misaligned between runs
% ----------------------------------------------------------------------
%%

addpath('[redacted]/Toolboxes/spm12');

cfg = get_cfg();
subjects = cfg.subjectNumbers;

for n = subjects
    subjectName = ['sub-', num2str(n, '%02d')];

    matlabbatch{1}.spm.spatial.realign.estimate.data = {
                                                        {
                                                        ['[redacted]/StudyForrest/func/', subjectName, '/ses-movie/func/', subjectName, '_ses-movie_task-movie_run-1_space-T1w_desc-unsmDenoised_bold.nii,1']
                                                        ['[redacted]/StudyForrest/func/', subjectName, '/ses-movie/func/', subjectName, '_ses-movie_task-movie_run-2_space-T1w_desc-unsmDenoised_bold.nii,1']
                                                        ['[redacted]/StudyForrest/func/', subjectName, '/ses-movie/func/', subjectName, '_ses-movie_task-movie_run-3_space-T1w_desc-unsmDenoised_bold.nii,1']
                                                        ['[redacted]/StudyForrest/func/', subjectName, '/ses-movie/func/', subjectName, '_ses-movie_task-movie_run-4_space-T1w_desc-unsmDenoised_bold.nii,1']
                                                        ['[redacted]/StudyForrest/func/', subjectName, '/ses-movie/func/', subjectName, '_ses-movie_task-movie_run-5_space-T1w_desc-unsmDenoised_bold.nii,1']
                                                        ['[redacted]/StudyForrest/func/', subjectName, '/ses-movie/func/', subjectName, '_ses-movie_task-movie_run-6_space-T1w_desc-unsmDenoised_bold.nii,1']
                                                        ['[redacted]/StudyForrest/func/', subjectName, '/ses-movie/func/', subjectName, '_ses-movie_task-movie_run-7_space-T1w_desc-unsmDenoised_bold.nii,1']
                                                        ['[redacted]/StudyForrest/func/', subjectName, '/ses-movie/func/', subjectName, '_ses-movie_task-movie_run-8_space-T1w_desc-unsmDenoised_bold.nii,1']
                                                        }
                                                        }';
   
    matlabbatch{1}.spm.spatial.realign.estimate.eoptions.quality = 0.9;
    matlabbatch{1}.spm.spatial.realign.estimate.eoptions.sep = 4;
    matlabbatch{1}.spm.spatial.realign.estimate.eoptions.fwhm = 5;
    matlabbatch{1}.spm.spatial.realign.estimate.eoptions.rtm = 0;
    matlabbatch{1}.spm.spatial.realign.estimate.eoptions.interp = 7;
    matlabbatch{1}.spm.spatial.realign.estimate.eoptions.wrap = [0 0 0];
    matlabbatch{1}.spm.spatial.realign.estimate.eoptions.weight = '';
    
    spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);

    
end
