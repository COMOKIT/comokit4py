#!/usr/bin/python3

##################################################
## Python script to generate XML to launch batch exploration of COMOKIT
## To use it you should write it like so :
#
## $ python3 generateMultipleXML.py -xml experimentName /path/to/file.gaml /path/to/export.xml
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMOKIT-HPC
## Licence: LGPL 3.0
## Version: 1.3.0
## Maintainer: RoiArthurB
##################################################

import sys, os
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

	result["varName"] = removeEndLine( line.split("var:")[1] )

	# Damien's particular variable
	if result["varName"] == "force_parameters":
		result = None
	else:
		result["name"] = line.split("\"")[1]
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
	
	# It's an explicite parameter
	if stringExtractor == "pa":
		result = extract_ExperimentLine(parameterLine)
	# It's within a facet
	else :
		pass

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
	parser.add_argument('-r', '--replication', metavar='INT', help="Number of replication for each paramater space", default=1, type=int)
	parser.add_argument('-s', '--split', metavar='INT', help="Split XML file every S replications", default=-1, type=int)
	parser.add_argument('-f', '--final', metavar='INT', help="Final step for simulations", default=-1, type=int)
	parser.add_argument('-o', '--output', metavar='STR', help="Path to folder where save output CSV", default="../../batch_output", type=str)
	parser.add_argument('-u', '--until', metavar='STR', help="Stop condition for the simulations", default="world.sim_stop()", type=str)
	parser.add_argument('-S', '--seed', metavar='INT', help="Starting value for seeding simulation", default=0, type=int)	
	parser.add_argument('-xml', metavar=("<experiment name>", "/path/to/file.gaml", "/path/to/file.xml"), nargs = 3, help = 'Classical xml arguments', required=True)
	args = parser.parse_args()

	expName, gamlFilePath, xmlFilePath = args.xml
	
	# Turn them all in absolute path
	gamlFilePath = os.path.abspath(gamlFilePath)
	xmlFilePath = os.path.abspath(xmlFilePath)
	args.output = os.path.abspath(args.output)

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
	print("\tNumber of exp in file : " + str(args.split))
	print("\tFinal step : " + str(args.final))

	# 4 _ Generate XML
	# 
	print("=== Start generating XML file :\n(every dot will be a simulation with all the replications created)")

	# Create output
	os.makedirs( os.path.dirname(xmlFilePath), exist_ok=True)

	# Create XML
	root = ET.Element("Experiment_plan")
	xmlNumber = 0
	seed = args.seed
	# Number of replication for every simulation
	for i in range(args.replication):
		# Every dot in the explorable universe
		for k in range(len(allParamValues)):
			resultSubFolder = ""
			
			simu = ET.SubElement(root, "Simulation", {
				"id"		: str( seed ),
				"seed"		: str( seed ),
				"experiment": expName,
				"until"		: str(args.until),
				"sourcePath": gamlFilePath
				})
			if args.final != -1:
				simu.set("finalStep", str(args.final))

			parameters = ET.SubElement(simu, "Parameters")
			# Set values for every parameters in the experiment
			for j in range(len(parametersList)):
				
				resultSubFolder += parametersList[j]["varName"] + "_" + str(allParamValues[k][j]) + "-"

				# Set exploration point
				ET.SubElement(parameters, "Parameter", {
					"name"	: parametersList[j]["name"],
					"type"	: parametersList[j]["type"],
					"value" : str(allParamValues[k][j]),
					"var"	: parametersList[j]["varName"]
					})
			# Set simulation id for csv name
			ET.SubElement(parameters, "Parameter", {
				"type"	: "INT",
				"value" : str( seed ),
				"var"	: "idSimulation"
				})
			# Set batch_output Path
			ET.SubElement(parameters, "Parameter", {
				"type"	: "STRING",
				"value" : args.output + "/" + resultSubFolder[:-1] + "/",
				"var"	: "result_folder"
				})
			ET.SubElement(simu, "Outputs")

			if( len(list(root)) >= args.split and args.split != -1):
				tree = ET.ElementTree(root)
				tree.write(xmlFilePath[:-4]+"-"+str(xmlNumber)+".xml")
				
				root = ET.Element("Experiment_plan");
				xmlNumber = xmlNumber + 1

			# Prepare for next loop
			seed = seed +1

		sys.stdout.write('.')
		sys.stdout.flush()

	print("\n=== Start saving XML file")
	tree = ET.ElementTree(root)
	if xmlNumber == 0:
		tree.write(xmlFilePath)
	else:
		tree.write(xmlFilePath[:-4]+"-"+str(xmlNumber)+".xml")
	print("\n=== Done ;)")