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
		result = splittedLine.split(";")[0].split(":")[0]

		# Among parsing => Keep array form
		if "[" not in result:
			result = result.split(" ")[-2]
		
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
		"value_among": "",
		"varName": "",
		"condition": False
	}

	result["varName"] = removeEndLine( line.split("var:")[1] )

	# Damien's particular variable
	if result["varName"] == "force_parameters":
		result = None
	else:
		# Normal line
		result["name"] = line.split("\"")[1]
		result["value_inital"] = removeEndLine( line.split("init:")[1] ).replace(" ", "")

		if (result["value_inital"] == "true") or (result["value_inital"] == "false"):
			result["value_among"] = result["value_inital"]
			result["type"] = "BOOLEAN"

		else:
			if "among" not in line: 
				result["value_min"] = removeEndLine( line.split("min:")[1] )
				result["value_max"] = removeEndLine( line.split("max:")[1] )
				result["value_step"] = removeEndLine( line.split("step:")[1] )
			else:
				result["value_among"] = removeEndLine( line.split("among:")[1] )
			
			if '.' in result["value_inital"]: 
				result["type"] = "FLOAT"

		# Check if condition apply
		if "if:" in line:
			result["condition"] = line.split("if:")[1][2:-1] 

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

def autoIndexSelector( argsFName ):
	path, tail = os.path.split( argsFName )

	return len([f for f in os.listdir(path) 
		if (tail[:-4] in f) and os.path.isfile(os.path.join(path, f))])

def generateExperimentUniverse(gamlFilePath):

	# Turn them all in absolute path
	gamlFilePath = os.path.abspath(gamlFilePath)

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
		# BOOLEAN variables
		if parameter["type"] == "BOOLEAN":
			t.extend(parameter["value_among"].split(" ")) #["true", "false"])
		elif parameter["value_among"] != "":
			t.extend(parameter["value_among"].replace("[", "").replace("]", "").replace(" ", "").split(","))
		else:
			for i in numpy.arange(float(parameter["value_min"]), float(parameter["value_max"]) + float(parameter["value_step"]), float(parameter["value_step"])):
				t.append( round(i, len(parameter["value_step"])) )
		allParamValues.append( t )

	# 3 _ Calculate all the possible universe
	#	https://www.geeksforgeeks.org/python-all-possible-permutations-of-n-lists/
	return [list(itertools.product(*allParamValues)), parametersList]

def createXmlFiles(allParamValues, parametersList, xmlFilePath, replication = 1, split = -1, output = "../../batch_output", seed = 0, final = -1, until = ""):

	xmlFilePath = os.path.abspath(xmlFilePath)
	
	# Prevent wrong path
	if output[-1] == "/":
		output = output[:-1]

	# Create output
	os.makedirs( os.path.dirname(xmlFilePath), exist_ok=True)

	# Create XML
	root = ET.Element("Experiment_plan")
	new_allParamValues = []
	hasCondition = False
	xmlNumber = autoIndexSelector( xmlFilePath )
	localSeed = seed
	# Number of replication for every simulation
	for i in range(replication):
		# Every dot in the explorable universe
		for k in range(len(allParamValues)):
			resultSubFolder = ""
			
			simu = ET.SubElement(root, "Simulation", {
				"id"		: str( localSeed - seed ),
				"seed"		: str( localSeed ),
				"experiment": expName,
				"sourcePath": gamlFilePath
				})
			if final != -1:
				simu.set("finalStep", str(final))
			if until != "":
				simu.set("until", str(until))

			parameters = ET.SubElement(simu, "Parameters")
			# Set values for every parameters in the experiment
			for j in range(len(parametersList)):

				# Set exploration point
				canWriteParameter = False
				if parametersList[j]["condition"] == False:
					canWriteParameter = True
				else:
					condition = parametersList[j]["condition"].split(",")
					for p in parameters:
						if p.get("var") == condition[0] and p.get("value") == condition[1]:
							canWriteParameter = hasCondition = True

				if canWriteParameter:
					ET.SubElement(parameters, "Parameter", {
						"name"	: parametersList[j]["name"],
						"type"	: parametersList[j]["type"],
						"value" : str(int(allParamValues[k][j])) if parametersList[j]["type"] == "INT" else str(allParamValues[k][j]),
						"var"	: parametersList[j]["varName"]
						})
				
					resultSubFolder += parametersList[j]["varName"] + "_" + str(allParamValues[k][j]) + "-"

			# Set batch_output Path
			ET.SubElement(parameters, "Parameter", {
				"type"	: "STRING",
				"value" : output + "/" + resultSubFolder[:-1],
				"var"	: "result_folder"
				})

			# On first round, prevent duplicated simulation (caused by condition)
			# + create new universe space list (without these duplication)
			duplicate = False
			if i == 0 and hasCondition:

				for sim in reversed(root[:-1]):
					if ET.tostring(parameters, encoding='unicode').replace("</Parameters>", "") in ET.tostring(sim, encoding='unicode') :
						duplicate = True
						break

				if duplicate:
					# Remove duplicated element from XML
					root.remove(root[-1])
				else:
					# Create cleared parameter list
					new_allParamValues.append(allParamValues[k])

			# Set simulation id for csv name
			ET.SubElement(parameters, "Parameter", {
				"type"	: "INT",
				"value" : str( localSeed - seed ),
				"var"	: "idSimulation"
				})
			ET.SubElement(simu, "Outputs")

			# Write and flush XML root if have to split
			if( len(list(root)) >= split and split != -1):
				tree = ET.ElementTree(root)
				tree.write(xmlFilePath[:-4]+"-"+str(xmlNumber)+".xml")
				
				root = ET.Element("Experiment_plan");
				xmlNumber = xmlNumber + 1

			# Prepare for next loop
			localSeed = localSeed +1

		# Reset universe space list without duplicated simulations
		if i == 0 and len(new_allParamValues) > 0 and hasCondition:
			allParamValues = new_allParamValues

	# File write of the (last?) XML file
	tree = ET.ElementTree(root)
	if xmlNumber == 0:
		tree.write(xmlFilePath)
	elif len(root) > 0:
		tree.write(xmlFilePath[:-4]+"-"+str(xmlNumber)+".xml")

	return True

#
#	MAIN
#
if __name__ == '__main__':

	# 0 _ Get/Set parameters
	# 
	parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options] -f INT -xml <experiment name> /path/to/file.gaml /path/to/file.xml')
	parser.add_argument('-r', '--replication', metavar='INT', help="Number of replication for each paramater space (default: 1)", default=1, type=int)
	parser.add_argument('-s', '--split', metavar='INT', help="Split XML file every S replications (default: 1)", default=-1, type=int)
	parser.add_argument('-o', '--output', metavar='STR', help="Relative path from GAML file to folder where save output CSV (default: \"../../batch_output\" => /path/to/COMOKIT/batch_output)", default="../../batch_output", type=str)
	parser.add_argument('-u', '--until', metavar='STR', help="Stop condition for the simulations (default: \"world.sim_stop()\"", default="", type=str)
	parser.add_argument('-S', '--seed', metavar='INT', help="Starting value for seeding simulation (default: 0)", default=0, type=int)	
	parser.add_argument('-f', '--final', metavar='INT', help="Final step for simulations", default=-1, type=int,  required=True)
	parser.add_argument('-xml', metavar=("<experiment name>", "/path/to/file.gaml", "/path/to/file.xml"), nargs = 3, help = 'Classical xml arguments', required=True)
	args = parser.parse_args()

	expName, gamlFilePath, xmlFilePath = args.xml

	# 1 _ Gather all parameters
	# 
	allParamValues, parametersList = generateExperimentUniverse(gamlFilePath)

	print("Total number of possible combinaison : " + str(len(allParamValues)))

	# 3.1 _ Inform for whole parameters
	print("\tReplications : " + str(args.replication))
	print("\tNumber of exp in file : " + (str(args.split) if args.split != -1 else 'All') )
	print("\tFinal step : " + str(args.final))

	# 4 _ Generate XML
	# 
	print("=== Start generating XML files...\n")

	print("\tNote : Real total number of simulation is " + str(len(allParamValues) * args.replication))

	if createXmlFiles(allParamValues, parametersList, xmlFilePath, args.replication, args.split, os.path.abspath(os.path.split(gamlFilePath)[0] + "/" + args.output), args.seed, args.final, args.until) :
		print("\n=== Done ;)")
	else:
		print("\n=== Error :(")