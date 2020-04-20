#!/usr/bin/python3

##################################################
## Python script to generate XML to launch batch exploration of COMOKIT
## To use it you should write it like so :
#
## $ python3 generateMultipleXML.py experimentName /path/to/file.gaml /path/to/export.xml
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMO-TK
## Licence: LGPL 3.0
## Version: 0.0.1
## Maintainer: RoiArthurB
##################################################

import sys

try:
	[t, expName, gamlFilePath, xmlFilePath] = sys.argv
except:
	print("Please use this script as followed :\n$ python3 generateMultipleXML.py experimentName /path/to/file.gaml /path/to/export.xml")
	raise

# 1 _ Gather all parameters
# 
# 2 _ Create list of possible values for every parameters
# 
# 3 _ Calculate all the possible universe
# 
# 4 _ Generate XML
