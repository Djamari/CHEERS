%-----------------------------------------------------------------------
% Per subject, per run, take the transformation matrix from the volume as
% computed by preproc1_align_between_runs.m and apply this matrix to all
% remaining volumes in the run.
% ----------------------------------------------------------------------

cfg = get_cfg();
subjects = cfg.subjectNumbers;

for n = subjects
    subjectName = ['sub-', num2str(n, '%02d')];
    dir_sub_func = ['[redacted]/StudyForrest/func/' , subjectName, '/ses-movie/func/'];
    
    disp('---------');
    disp(['Start of ', subjectName]);
    for r = 1:8
        file_read = [subjectName, '_ses-movie_task-movie_run-', num2str(r), '_space-T1w_desc-unsmDenoised_bold.nii'];

        % Load the data
        hdr = spm_vol([dir_sub_func, file_read]);

        % Get transformation matrix from first frame of this run
        transformation_matrix = hdr(1).mat;

        % Change mat field in remaining frames
        for frame = 2:length(hdr)
            hdr(frame).mat = transformation_matrix;
        end

        % Save the file
        disp(['Saving file: run ', num2str(r)]);
        data = spm_read_vols(hdr);
        new_filename = [dir_sub_func, 'aligned_', file_read];
        n = length(hdr);
        for f=1:n
            hdr(f).fname=new_filename;
            hdr(f).private.dat.fname = hdr(f).fname;
            spm_write_vol(hdr(f),data(:,:,:,f));
        end
        disp('Done saving file');
    end
end