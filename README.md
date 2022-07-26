# Steps for processing fmri data using fmriprep, Tedana and ANTs

This code was developed by HAM Lab Otago University as a test for our internal data processing pipeline and not intended for external use. Use with caution!

## Prerequisites

* [fmriprep-docker](https://fmriprep.org/en/stable/installation.html)
* [Tedana](https://tedana.readthedocs.io/en/stable/installation.html)
* [ANTs](https://github.com/ANTsX/ANTs/wiki/Compiling-ANTs-on-Linux-and-Mac-OS)

Note: Be sure to configure docker to be run as a user, this is important to avoid output files being owned by root, which can lead to problems down the track.

### Step 1

Configure file paths inside the file step_1_fmri.sh
Run script using $ sh step_1_fmri.sh

### Step 2 

Configure file paths inside the file step_2_fmri.sh
Run script using $ sh step_2_fmri.sh

### Step 3

Configure file paths inside the file step_3_tedana.py
Note: Make sure to activate your virtual enviroment if you are using conda or another Python package manager
Run script using $ python step_3_tedana.sh

### Step 4

Configure file paths inside the file step_4_ants.sh
Run script using $ sh step_4_ants.sh
