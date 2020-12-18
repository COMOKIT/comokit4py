#!/bin/bash

##################################################
## Bash script to change COMOKIT path from generated XML
## $ bash fixMyComokitPath.sh -n /path/to/COMOKIT-Model/COMOKIT -x /path/to/file.xml
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMOKIT-HPC
## Licence: LGPL 3.0
## Version: 1.0.0
## Maintainer: RoiArthurB
##################################################

newComokitPath=""
oldComokitPath="/home/roiarthurb/Documents/COMOKIT/Model/COMOKIT"
xmlPath=""

while getopts n:x:c: option
do
	case "${option}" in
		n) newComokitPath=${OPTARG};;
		x) xmlPath=${OPTARG};;
		c) oldComokitPath=${OPTARG};;
	esac
done

# Check if sed is install
if ! [ -x "$(command -v sed)" ]; then
  echo 'Error: sed is not installed.' >&2
  exit 1
fi

echo "s/$oldComokitPath/$newComokitPath/g $xmlPath"

sed -i 's|'$oldComokitPath'|'$newComokitPath'|g' $xmlPath