import os
import comokit4py.generateMultipleXML as gen
import xmldiff

base = os.path.dirname(__file__)
replication = 1
split = -1
seed = 0
final = 1
until = ""

def runtests():
	originalXmlFile = os.path.join(base, "Original.xml")
	gamlFile = os.path.join(base, "TestExperiment.gaml")
	expName = "HeadlessComparison"
	xmlFile = os.path.join(base, "Output.xml")
	allParamValues, parametersList = gen.generateExperimentUniverse(gamlFile, expName)
	gen.createXmlFiles(
			expName,
			gamlFile,
			allParamValues,
			parametersList,
			xmlFile,
			replication,
			split,
			base,
			seed,
			final,
			until)
	result = xmldiff.diff(xmlFile, originalXmlFile) 
	os.remove(xmlFile)
	return result
