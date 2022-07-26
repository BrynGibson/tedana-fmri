import pandas as pd
from tedana import workflows
import json
import os
import re
import time
from pathlib import Path


# Output from frmiprep in step 2
prep_data = "/home/gibbr625/MeiLiv/MeiLivData/test1-25May2022/derivatives_W_me_output_echos"

# base bids data directory
bids_dir= "/home/gibbr625/MeiLiv/MeiLivData/test1-25May2022/pilotData"


# # Obtain Echo files
#find the prefix and suffix to that echo #
echo_images=[f for root, dirs, files in os.walk(prep_data) for f in files if ('_echo-' in f)& (f.endswith('_bold.nii.gz'))]

#Make a list of filenames that match the prefix
image_prefix_list=[re.search('(.*)_echo-',f).group(1) for f in echo_images]
image_prefix_list=set(image_prefix_list)

#Make a dataframe where C1 is Sub C2 is inputFiles and C3 is Echotimes
data=[]
for acq in image_prefix_list:
    #Use RegEx to find Sub
    sub="sub-"+re.search('sub-(.*)_task',acq).group(1)
    #Make a list of the json's w/ appropriate header info from BIDS
    ME_headerinfo=[os.path.join(root, f) for root, dirs, files in os.walk(bids_dir) for f in files if (acq in f)& (f.endswith('_bold.json'))]

    #Read Echo times out of header info and sort
    echo_times=[json.load(open(f))['EchoTime'] for f in ME_headerinfo]
    echo_times.sort()

    #Find images matching the appropriate acq prefix
    acq_image_files=[os.path.join(root, f) for root, dirs, files in os.walk(prep_data) for f in files if (acq in f) & ('echo' in f) & (f.endswith('_desc-preproc_bold.nii.gz'))]
    acq_image_files.sort()
    
    res = re.search('MB\dME', acq_image_files[0]).group(0)
    
    out_dir= os.path.join(
        os.path.abspath(
            os.path.dirname( prep_data )), f"tedana/{sub}/{res}")

    print(prep_data,out_dir)

    data.append([sub,acq_image_files,echo_times,out_dir])

InData_df=pd.DataFrame(data=data,columns=['sub','EchoFiles','EchoTimes','OutDir'])
args=zip(InData_df['sub'].tolist(),
        InData_df['EchoFiles'].tolist(),
        InData_df['EchoTimes'].tolist(),
        InData_df['OutDir'].tolist())

  #Changes can be reasonably made to
  #fittype: 'loglin' is faster but maybe less accurate than 'curvefit'
  #tedpca:'mdl'Minimum Description Length returns the least number of components (default) and recommeded
  #'kic' Kullback-Leibler Information Criterion medium aggression
  # 'aic' Akaike Information Criterion least aggressive; i.e., returns the most components.
  #gscontrol: post-processing to remove spatially diffuse noise. options implemented here are...
  #global signal regression (GSR), minimum image regression (MIR),
  #But anatomical CompCor, Go Decomposition (GODEC), and robust PCA can also be used

def RUN_Tedana(sub,EchoFiles,EchoTimes,OutDir):

    time.sleep(2)
    print(sub+'\n')

    if not os.path.isdir(OutDir):
        Path.mkdir(Path(OutDir),exist_ok=True, parents=True)
        
    else:
        workflows.tedana_workflow(
        EchoFiles,
        EchoTimes,
        out_dir=OutDir,
        prefix="%s_task-tap_acq_space-Native"%(sub), # set filename prefix for output 
        fittype="curvefit",
        tedpca="kic",
        verbose=True,
        gscontrol=None)


if __name__ == "__main__":

    for arg in args:
        RUN_Tedana(*arg)
    