%-----------------------------------------------------------------------
% Creates final GM mask that also only includes voxels that were measured
% in all subjects, and can be considered gray matter based on tpm_3mm.
%-----------------------------------------------------------------------
%%
matlabbatch{1}.spm.util.imcalc.input = {                                       
                                        '[redacted]/StudyForrest/data raw/func/sub-01/ses-movie/func/mask_sub-01_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-02/ses-movie/func/mask_sub-02_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-03/ses-movie/func/mask_sub-03_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-04/ses-movie/func/mask_sub-04_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-05/ses-movie/func/mask_sub-05_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-06/ses-movie/func/mask_sub-06_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-09/ses-movie/func/mask_sub-09_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-10/ses-movie/func/mask_sub-10_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-14/ses-movie/func/mask_sub-14_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-15/ses-movie/func/mask_sub-15_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-16/ses-movie/func/mask_sub-16_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-17/ses-movie/func/mask_sub-17_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-18/ses-movie/func/mask_sub-18_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-19/ses-movie/func/mask_sub-19_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/func/sub-20/ses-movie/func/mask_sub-20_measured_voxels.nii,1'
                                        '[redacted]/StudyForrest/data raw/masks/tpm_3mm.nii,1'
                                        };
%%
matlabbatch{1}.spm.util.imcalc.output = 'GM_mask';
matlabbatch{1}.spm.util.imcalc.outdir = {'[redacted]/StudyForrest/data raw/masks/'};
matlabbatch{1}.spm.util.imcalc.expression = '(i16 > 0.35 & i3  > 0 & i4  > 0 & i5  > 0 & i6  > 0 & i7  > 0 & i8  > 0 & i9  > 0 & i10  > 0 & i11  > 0 & i12  > 0 & i13  > 0 & i14  > 0 & i15  > 0 & i1  > 0 & i2  > 0 )';
matlabbatch{1}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{1}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{1}.spm.util.imcalc.options.mask = 0;
matlabbatch{1}.spm.util.imcalc.options.interp = 5;
matlabbatch{1}.spm.util.imcalc.options.dtype = 4;

spm('defaults', 'FMRI');
spm_jobman('run', matlabbatch);
