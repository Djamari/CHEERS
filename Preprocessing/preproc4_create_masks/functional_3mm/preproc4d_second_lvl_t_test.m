%-----------------------------------------------------------------------
% Perform a t-test across subjects to determine which voxels are active for
% specific image categories at the group-level 
% Note: this does not include creating the SPM.mat files and model estimation, 
% as this was done in the SPM GUI
%-----------------------------------------------------------------------




clear all;
cope = 6; %6 for VIS, 3 for RSC/PPA

matlabbatch{1}.spm.stats.factorial_design.dir = {['/home/djaoet/u616185/PhD/H1/Scripts/Preprocessing/create masks/functional_3mm/results_cope', num2str(cope)]};
%%
matlabbatch{1}.spm.stats.factorial_design.des.t1.scans = {
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-01/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-02/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-03/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-04/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-05/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-06/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-09/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-10/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-14/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-15/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-16/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-17/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-18/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-19/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          ['/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/functional localizer/sub-20/2ndlvl.gfeat/cope', num2str(cope), '.feat/stats/wcope1.nii,1']
                                                          };
%%
matlabbatch{1}.spm.stats.factorial_design.cov = struct('c', {}, 'cname', {}, 'iCFI', {}, 'iCC', {});
matlabbatch{1}.spm.stats.factorial_design.multi_cov = struct('files', {}, 'iCFI', {}, 'iCC', {});
matlabbatch{1}.spm.stats.factorial_design.masking.tm.tm_none = 1;
matlabbatch{1}.spm.stats.factorial_design.masking.im = 1;
matlabbatch{1}.spm.stats.factorial_design.masking.em = {''};
matlabbatch{1}.spm.stats.factorial_design.globalc.g_omit = 1;
matlabbatch{1}.spm.stats.factorial_design.globalm.gmsca.gmsca_no = 1;
matlabbatch{1}.spm.stats.factorial_design.globalm.glonorm = 1;

spm('defaults', 'FMRI');
spm_jobman('run', matlabbatch);