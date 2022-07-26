#!/bin/bash -e

# subject id
subject="sub-001"

# echos to process
echos="MB1ME MB2ME MB4ME"

for echo in $echos
do
echo "starting ${echo}"

# path to fmriprep output from step 2
fmriprep_dir="/home/gibbr625/MeiLiv/MeiLivData/test1-25May2022/derivatives_W_me_output_echos/${subject}/ses-1"

# path to tedana output from step 3
tedana_dir="/home/gibbr625/MeiLiv/MeiLivData/test1-25May2022/tedana/${subject}_ses-1/${echo}"


# Result of denoising the scanner-space multi-echo data with tedana
file_to_warp="${tedana_dir}/${subject}_ses-1_task-tap_acq_space-Native_desc-optcomDenoised_bold.nii.gz"

# Name of the standard-space denoised data file to be written out
out_file="${fmriprep_dir}/func/${subject}_ses-1_task-tap_acq-${echo}_space-MNI152NLin2009cAsym-desc-optcomDenoised_bold.nii.gz"

# An existing standard-space
standard_space_file="${fmriprep_dir}/func/${subject}_ses-1_task-tap_acq-${echo}_space-MNI152NLin2009cAsym_boldref.nii.gz"

# Transforms
xform_native_to_t1w="${fmriprep_dir}/anat/${subject}_ses-1_from-fsnative_to-T1w_mode-image_xfm.txt"
xform_t1w_to_std="${fmriprep_dir}/anat/${subject}_ses-1_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5"

antsApplyTransforms \
    -e 3 \
    -i ${file_to_warp} \
    -r ${standard_space_file} \
    -o ${out_file} \
    -n LanczosWindowedSinc \
    -t ${xform_native_to_t1w} \
    ${xform_t1w_to_std}

echo "finshed ${echo}"
done