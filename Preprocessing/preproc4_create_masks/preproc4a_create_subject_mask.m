%-----------------------------------------------------------------------
% Creates a mask per subject that only includes voxels that were actually
% measured by thresholding the functional data of each run.
%-----------------------------------------------------------------------

cfg = get_cfg();
subjects = cfg.subjectNumbers;


for n = subjects
    subjectName = ['sub-', num2str(n, '%02d')];
    matlabbatch{1}.spm.util.imcalc.input = {
                                            ['[redacted]/StudyForrest/data raw/func/', subjectName, '/ses-movie/func/waligned_', subjectName, '_ses-movie_task-movie_run-1_space-T1w_desc-unsmDenoised_bold.nii,1']
                                            ['[redacted]/StudyForrest/data raw/func/', subjectName, '/ses-movie/func/waligned_', subjectName, '_ses-movie_task-movie_run-2_space-T1w_desc-unsmDenoised_bold.nii,1']
                                            ['[redacted]/StudyForrest/data raw/func/', subjectName, '/ses-movie/func/waligned_', subjectName, '_ses-movie_task-movie_run-3_space-T1w_desc-unsmDenoised_bold.nii,1']
                                            ['[redacted]/StudyForrest/data raw/func/', subjectName, '/ses-movie/func/waligned_', subjectName, '_ses-movie_task-movie_run-4_space-T1w_desc-unsmDenoised_bold.nii,1']
                                            ['[redacted]/StudyForrest/data raw/func/', subjectName, '/ses-movie/func/waligned_', subjectName, '_ses-movie_task-movie_run-5_space-T1w_desc-unsmDenoised_bold.nii,1']
                                            ['[redacted]/StudyForrest/data raw/func/', subjectName, '/ses-movie/func/waligned_', subjectName, '_ses-movie_task-movie_run-6_space-T1w_desc-unsmDenoised_bold.nii,1']
                                            ['[redacted]/StudyForrest/data raw/func/', subjectName, '/ses-movie/func/waligned_', subjectName, '_ses-movie_task-movie_run-7_space-T1w_desc-unsmDenoised_bold.nii,1']
                                            ['[redacted]/StudyForrest/data raw/func/', subjectName, '/ses-movie/func/waligned_', subjectName, '_ses-movie_task-movie_run-8_space-T1w_desc-unsmDenoised_bold.nii,1']
                                            };
    matlabbatch{1}.spm.util.imcalc.output = ['mask_', subjectName , '_measured_voxels'];
    matlabbatch{1}.spm.util.imcalc.outdir = {['[redacted]/StudyForrest/data raw/func/', subjectName, '/ses-movie/func']};
    matlabbatch{1}.spm.util.imcalc.expression = 'i1 > 0.8 * nanmean(i1, ''all'') & i2 > 0.8 * nanmean(i2, ''all'') & i3 > 0.8 * nanmean(i3, ''all'') & i4 > 0.8 * nanmean(i4, ''all'') & i5 > 0.8 * nanmean(i5, ''all'') & i6 > 0.8 * nanmean(i6, ''all'') & i7 > 0.8 * nanmean(i7, ''all'') & i8 > 0.8 * nanmean(i8, ''all'')';
    matlabbatch{1}.spm.util.imcalc.var = struct('name', {}, 'value', {});
    matlabbatch{1}.spm.util.imcalc.options.dmtx = 0;
    matlabbatch{1}.spm.util.imcalc.options.mask = 0;
    matlabbatch{1}.spm.util.imcalc.options.interp = 7;
    matlabbatch{1}.spm.util.imcalc.options.dtype = 4;

    spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);
end
