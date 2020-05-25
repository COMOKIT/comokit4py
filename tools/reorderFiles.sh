#!/bin/bash

##################################################
## Bash script to reorder files if badly saved from exploration
## To use it you should move to batch_output (with all .csv) and launch this script
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMOKIT-HPC
## Licence: LGPL 3.0
## Version: 1.0.0
## Maintainer: RoiArthurB
##################################################

# Create sub folder and move corresponding files in
for file in *; do dir=$(echo $file | cut -dD -f1); mkdir -p $dir; mv $file $dir; done
# Rename folders
for file in *; do mv "${file}" "${file/batch/}"; done
# Go in every subfolder and rename files within
for directory in *; do cd $directory; for file in *; do dir=$(echo $file | cut -dD -f2); mv $file $dir; done; for i in *; do mv "$i" batchD"$i"; done; cd ..; done
