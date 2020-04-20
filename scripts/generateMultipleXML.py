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
import numpy
import itertools 

#
#	VARIABLES
#

parametersList = []

#
#	FUNCTIONS
#

def removeEndLine (splittedLine):
	try:
		result = splittedLine.split(";")[0].split(":")[0].split(" ")[-2]
		if result == "":
			raise
	except:
		result = splittedLine.split(";")[0]

	return result

def extract_ExperimentLine( line ):
	result = {
		"name" : "",
		"type": "INT",
		"value_inital": "",
		"value_min": "0",
		"value_max": "",
		"value_step": "1",
		"varName": ""
	}

	result["name"] = line.split("\"")[1]
	result["varName"] = removeEndLine( line.split("var:")[1] )
	result["value_inital"] = removeEndLine( line.split("init:")[1] )

	if isinstance(result["value_inital"], bool):
		result["value_min"] = "0"
		result["value_max"] = "1"
		result["value_step"] = "1"
		result["type"] = "BOOL"

	else:
		result["value_min"] = removeEndLine( line.split("min:")[1] )
		result["value_max"] = removeEndLine( line.split("max:")[1] )
		result["value_step"] = removeEndLine( line.split("step:")[1] )
		
		if '.' in result["value_inital"]: 
			result["type"] = "FLOAT"


	return result

def extract_VariableLine( line ):
	result = {
		"name" : "",
		"type": "INT",
		"value_inital": "",
		"value_min": "0",
		"value_max": "",
		"value_step": "1",
		"varName": ""
	}

	result["name"] = result["varName"] = removeEndLine( line.split(" ")[1] )
	result["type"] = line.split(" ")[0].capitalize()
	result["value_inital"] = removeEndLine( line.split("<-")[1] )
	if result["type"] == "BOOL":
		result["value_max"] = "1"
	else:
		result["value_min"] = removeEndLine( line.split("min:")[1] )
		result["value_max"] = removeEndLine( line.split("max:")[1] )
		result["value_step"] = removeEndLine( line.split("step:")[1] )
	
	return result

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
# 
with open(gamlFilePath) as f:
	for l in f.readlines():
		if "parameter" in l: 
			temp = extractParametersAttributes( l.strip()  )
			if temp is not None:
				parametersList.append( extractParametersAttributes( l.strip()  ) )

# 2 _ Create list of possible values for every parameters
# 
allParamValues = []
for parameter in parametersList:
	t = []
	for i in numpy.arange(float(parameter["value_min"]), float(parameter["value_max"]) + float(parameter["value_step"]), float(parameter["value_step"])):
		t.append(i)
	allParamValues.append( t )

# 3 _ Calculate all the possible universe
#	https://www.geeksforgeeks.org/python-all-possible-permutations-of-n-lists/
res = list(itertools.product(*allParamValues)) 
print(len(res))

# 4 _ Generate XML
# 
