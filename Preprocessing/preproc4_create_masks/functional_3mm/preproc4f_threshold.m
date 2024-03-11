close all;
clear all;
clc;

ROI = 'VIS_R'; % PPA_L, PPA_R, RSC_L, RSC_R, VIS_L, VIS_R

% Get coordinates of a voxel that is at least at the right location, and 
% the threshold for this ROI.
% The coordinates are based on visual inspection in combination with
% expected location per ROI.
% The thresholds are based on the results in preproc4e_try_thresholds.m
switch(ROI)
    case 'PPA_L'
        x_org = 23;
        y_org = 27;
        z_org = 22;
        cope = 3;
        theta = 4.5;
    case 'PPA_R'
        x_org = 39;
        y_org = 27;
        z_org = 21;
        cope = 3;
        theta = 5.79;
    case 'RSC_L'
        x_org = 26;
        y_org = 24;
        z_org = 28;
        cope = 3;
        theta = 4.36;
    case 'RSC_R'
        x_org = 36;
        y_org = 25;
        z_org = 31;
        cope = 3;
        theta = 4.55;
    case 'VIS_L'
        x_org = 28;
        y_org = 11;
        z_org = 30;
        cope = 6;
        theta = 3.5;
    case 'VIS_R'
        x_org = 35;
        y_org = 12;
        z_org = 29;
        cope = 6;
        theta = 3.39;
end

% Correct x value
x_org = 62 - x_org;

map_dir = ['/home/djaoet/u616185/PhD/H1/Scripts/Preprocessing/create masks/functional_3mm/results_cope', num2str(cope), '/'];

% Load GM-mask
filename = '/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/masks/GM_mask.nii';
hdr = spm_vol(filename);
mask = spm_read_vols(hdr);

% Load t-values
filename = [map_dir, 'spmT_0001.nii'];
hdr = spm_vol(filename);
t_values =spm_read_vols(hdr);

% Mask
t_values = mask .* t_values;


% In case of VIS, remove midline
if strcmp(ROI, 'VIS_L') || strcmp(ROI,'VIS_R')
    t_values(31:32,:,:) = 0; % x = 31.5 is midline  
end


% Find isolated cluster
search_tree = [x_org,y_org,z_org];
visited = zeros(size(t_values));
map_cluster = zeros(size(t_values));

while size(search_tree,1) > 0
   % Get next voxel to check
   x = search_tree(1,1);
   y = search_tree(1,2);
   z = search_tree(1,3);

   % Only get neighbours when not yet visited
   if visited(x,y,z) == 0

       % Set visited to 1
       visited(x,y,z) = 1;

       % Check if voxel survives thresholding
       if t_values(x,y,z) > theta
           % Add to cluster
           map_cluster(x,y,z) = 1;

           % Compute neighbours and add them to search_tree
           search_tree = [search_tree; [x-1, y, z]];
           search_tree = [search_tree; [x+1, y, z]];
           search_tree = [search_tree; [x, y-1, z]];
           search_tree = [search_tree; [x, y+1, z]];
           search_tree = [search_tree; [x, y, z-1]];
           search_tree = [search_tree; [x, y, z+1]];
       end

   end

   % Remove this voxel from search tree
   search_tree(1,:) = [];
end

% Count remaining number of voxels
count = sum(sum(sum(map_cluster)));
disp('-------')
disp(['Theta: ', num2str(theta)])
disp(['Voxels: ', num2str(count)]);

% Save nifti
map_ROI = '/home/djaoet/wrkgrp/Djamari/StudyForrest/data raw/masks/ROIs/';
hdr_new = hdr;
filename = [map_ROI, ROI, '.nii'];
hdr_new.fname = filename;
hdr.private.dat.fname = filename;
spm_write_vol(hdr_new, map_cluster);
