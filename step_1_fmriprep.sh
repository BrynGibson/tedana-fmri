#!/bin/bash -e

# path to base bids data
bids_path="/home/gibbr625/MeiLiv/MeiLivData/test1-25May2022/pilotData" 

# output path
out_path="/home/gibbr625/MeiLiv/MeiLivData/test1-25May2022/derivatives_WO_me_output_echos"

participant_id="sub-001"

# working dir, this should be a local filesystem with high I/O to be used as a temp working directory
work_dir_path="/home/gibbr625/fmriprep_working_dir"


fmriprep-docker ${bids_path} \ 
${out_path} \
participant --participant_label ${participant_id} \
--write-graph \
--notrack \
--fs-license-file /media/hcs-sci-psy-narun/MeiLiv/MeiLivData/license.txt \
--work-dir ${work_dir_path}