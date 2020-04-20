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

#
#	VARIABLES
#

parametersList = []

#
#	FUNCTIONS
#

def extract_ExperimentLine( line ):
	return line

def extract_VariableLine( line ):
	return line

def extractParametersAttributes( parameterLine ):
	stringExtractor = parameterLine[0:2]
	result = None
	
	# It's a comment => Drop
	if stringExtractor == "//":
		pass
	# It's without the experiment
	elif stringExtractor == "pa":
		result = extract_ExperimentLine(parameterLine)
	# It's within a facet
	else :
		result = extract_VariableLine(parameterLine)

	return result

try:
	[t, expName, gamlFilePath, xmlFilePath] = sys.argv
except:
	print("Please use this script as followed :\n$ python3 generateMultipleXML.py experimentName /path/to/file.gaml /path/to/export.xml")
	raise


#
#	MAIN
#

# 1 _ Gather all parameters
print(gamlFilePath)
with open(gamlFilePath) as f:
	for l in f.readlines():
		if "parameter" in l: 
			temp = extractParametersAttributes( l.strip()  )
			if temp is not None:
				parametersList.append( extractParametersAttributes( l.strip()  ) )

print(parametersList)
# 2 _ Create list of possible values for every parameters
# 
# 3 _ Calculate all the possible universe
# 
# 4 _ Generate XML
