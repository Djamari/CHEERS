%-----------------------------------------------------------------------
% Normalize the cope results of the functional localizer to MNI space,
% based on the parameters used to normalize movie data.
%-----------------------------------------------------------------------

cfg = get_cfg();
subjects = cfg.subjectNumbers;

for cope = [3,6]
    for n = subjects
        subjectName = ['sub-', num2str(n, '%02d')];
        
        matlabbatch{1}.spm.spatial.coreg.estwrite.ref = {['[redacted]/studyforrest-data-aligned/', subjectName,'/in_bold3Tp2/', subjectName,'_task-avmovie_run-1_bold.nii,1']};
        matlabbatch{1}.spm.spatial.coreg.estwrite.source = {['[redacted]/StudyForrest/data raw/anat/', subjectName,'/anat/', subjectName,'_T1w.nii,1']};
        matlabbatch{1}.spm.spatial.coreg.estwrite.other = {''};
        matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
        matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
        matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
        matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
        matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.interp = 7;
        matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
        matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.mask = 0;
        matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.prefix = 'r';
        matlabbatch{2}.spm.spatial.preproc.channel.vols(1) = cfg_dep('Coregister: Estimate & Reslice: Resliced Images', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','rfiles'));
        matlabbatch{2}.spm.spatial.preproc.channel.biasreg = 0.001;
        matlabbatch{2}.spm.spatial.preproc.channel.biasfwhm = 60;
        matlabbatch{2}.spm.spatial.preproc.channel.write = [0 1];
        matlabbatch{2}.spm.spatial.preproc.tissue(1).tpm = {'[redacted]/Toolboxes/spm12/tpm/TPM.nii,1'};
        matlabbatch{2}.spm.spatial.preproc.tissue(1).ngaus = 1;
        matlabbatch{2}.spm.spatial.preproc.tissue(1).native = [1 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(1).warped = [0 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(2).tpm = {'[redacted]/Toolboxes/spm12/tpm/TPM.nii,2'};
        matlabbatch{2}.spm.spatial.preproc.tissue(2).ngaus = 1;
        matlabbatch{2}.spm.spatial.preproc.tissue(2).native = [1 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(2).warped = [0 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(3).tpm = {'[redacted]/Toolboxes/spm12/tpm/TPM.nii,3'};
        matlabbatch{2}.spm.spatial.preproc.tissue(3).ngaus = 2;
        matlabbatch{2}.spm.spatial.preproc.tissue(3).native = [1 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(3).warped = [0 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(4).tpm = {'[redacted]/Toolboxes/spm12/tpm/TPM.nii,4'};
        matlabbatch{2}.spm.spatial.preproc.tissue(4).ngaus = 3;
        matlabbatch{2}.spm.spatial.preproc.tissue(4).native = [1 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(4).warped = [0 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(5).tpm = {'[redacted]/Toolboxes/spm12/tpm/TPM.nii,5'};
        matlabbatch{2}.spm.spatial.preproc.tissue(5).ngaus = 4;
        matlabbatch{2}.spm.spatial.preproc.tissue(5).native = [1 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(5).warped = [0 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(6).tpm = {'[redacted]/Toolboxes/spm12/tpm/TPM.nii,6'};
        matlabbatch{2}.spm.spatial.preproc.tissue(6).ngaus = 2;
        matlabbatch{2}.spm.spatial.preproc.tissue(6).native = [0 0];
        matlabbatch{2}.spm.spatial.preproc.tissue(6).warped = [0 0];
        matlabbatch{2}.spm.spatial.preproc.warp.mrf = 1;
        matlabbatch{2}.spm.spatial.preproc.warp.cleanup = 1;
        matlabbatch{2}.spm.spatial.preproc.warp.reg = [0 0.001 0.5 0.05 0.2];
        matlabbatch{2}.spm.spatial.preproc.warp.affreg = 'mni';
        matlabbatch{2}.spm.spatial.preproc.warp.fwhm = 0;
        matlabbatch{2}.spm.spatial.preproc.warp.samp = 3;
        matlabbatch{2}.spm.spatial.preproc.warp.write = [0 1];
        matlabbatch{2}.spm.spatial.preproc.warp.vox = NaN;
        matlabbatch{2}.spm.spatial.preproc.warp.bb = [NaN NaN NaN
                                                      NaN NaN NaN];
        matlabbatch{3}.spm.spatial.normalise.write.subj.def(1) = cfg_dep('Segment: Forward Deformations', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','fordef', '()',{':'}));
        matlabbatch{3}.spm.spatial.normalise.write.subj.resample = {['[redacted]/StudyForrest/data raw/functional localizer/', subjectName,'/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/cope1.nii,1']};
        matlabbatch{3}.spm.spatial.normalise.write.woptions.bb = [NaN NaN NaN
                                                                  NaN NaN NaN];
        matlabbatch{3}.spm.spatial.normalise.write.woptions.vox = [3 3 3];
        matlabbatch{3}.spm.spatial.normalise.write.woptions.interp = 7;
        matlabbatch{3}.spm.spatial.normalise.write.woptions.prefix = 'w';
        
        spm('defaults', 'FMRI');
        spm_jobman('run', matlabbatch);
        
    end
end
