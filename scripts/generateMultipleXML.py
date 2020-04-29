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
import xml.etree.ElementTree as ET
import argparse

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
	# Create simulation -> Wrong exp => Drop
	elif stringExtractor == "cr":
		pass
	# It's without the experiment
	elif stringExtractor == "pa":
		result = extract_ExperimentLine(parameterLine)
	# It's within a facet
	else :
		result = extract_VariableLine(parameterLine)

	#check if the variable hasn't already be saved
	for p in parametersList:
		if result != None and result["varName"] == p["varName"]:
			result = None
			break

	return result



#
#	MAIN
#
if __name__ == '__main__':

	# 0 _ Get/Set parameters
	# 
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--replication', metavar='INT', help="Number of replication for each paramater space", default=1000, type=int)
	parser.add_argument('-s', '--split', metavar='INT', help="Split XML file every S replications", default=-1, type=int)
	parser.add_argument('-f', '--final', metavar='INT', help="Final step for simulations", default=5000, type=int)
	parser.add_argument('-xml', metavar=("<experiment name>", "/path/to/file.gaml", "/path/to/file.xml"), nargs = 3, help = 'Classical xml arguments', required=True)
	args = parser.parse_args()

	expName, gamlFilePath, xmlFilePath = args.xml
	
	# 1 _ Gather all parameters
	# 
	with open(gamlFilePath) as f:
		for l in f.readlines():
			if "parameter" in l: 
				temp = extractParametersAttributes( l.strip()  )
				if temp is not None:
					parametersList.append( extractParametersAttributes( l.strip()  ) )
			#if expName in l:


	print("Total number of parameters detected : " + str(len(parametersList)))

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
	allParamValues = list(itertools.product(*allParamValues)) 

	print("Total number of possible combinaison : " + str(len(allParamValues)))

	# 3.1 _ Inform for whole parameters
	print("\tReplications : " + str(args.replication))
	print("\tNumber of file : " + str(args.split))
	print("\tFinal step : " + str(args.final))

	# 4 _ Generate XML
	# 
	print("=== Start generating XML file :\n(every dot will be a simulation with all the replications created)")
	root = ET.Element("Experiment_plan")
	xmlNumber = 0
	# Every dot in the explorable universe
	for k in range(len(allParamValues)):
		# Number of replication for every simulation
		for i in range(args.replication):
			simu = ET.SubElement(root, "Simulation", {
				"id"		: str( len(list(root.iter("Simulation"))) ),
				"experiment": expName,
				"finalStep"	: str(args.final),
				"sourcePath": gamlFilePath
				})
			parameters = ET.SubElement(simu, "Parameters")
			# Set values for every parameters in the experiment
			for j in range(len(parametersList)):
				ET.SubElement(parameters, "Parameter", {
					"name"	: parametersList[j]["name"],
					"type"	: parametersList[j]["type"],
					"value" : str(allParamValues[k][j]),
					"var"	: parametersList[j]["varName"]
					})
			# Set simulation id for csv name
			ET.SubElement(parameters, "Parameter", {
				"type"	: "INT",
				"value" : str( len(list(root.iter("Simulation"))) ),
				"var"	: "idSimulation"
				})
			ET.SubElement(simu, "Outputs")

			if( len(list(root)) >= args.split and args.split != -1):
				tree = ET.ElementTree(root)
				tree.write(xmlFilePath[:-4]+"-"+str(xmlNumber)+".xml")
				
				root = ET.Element("Experiment_plan");
				xmlNumber = xmlNumber + 1

		sys.stdout.write('.')
		sys.stdout.flush()

	print("\n=== Start saving XML file")
	tree = ET.ElementTree(root)
	if xmlNumber == 0:
		tree.write(xmlFilePath)
	else:
		tree.write(xmlFilePath[:-4]+"-"+str(xmlNumber)+".xml")
	print("\n=== Done ;)")