#!/usr/bin/python3

##################################################
## Short bio
#
## $ pip install comokit4py
## > import comokit4py
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2021, COMOKIT
## Licence: LGPL 3.0
## Maintainer: RoiArthurB
##################################################

import os, pkgutil
# Import all other py scripts
__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))

class Workspace:
	def __init__(self, gama : Gama, explorationPlan : GamaExploration, workspaceDirectory : str):
		"""
		Constructor for Workspace object

		:param gama: Gama object for launching exploration
		:param explorationPlan: GamaExploration object to know what to launch
		:param workspaceDirectory: Directory path when everything will be store

		:return: Workspace object
		"""
		self.gama = gama
		self.explorationPlan = explorationPlan
		self.outputDirectory = outputDirectory
	#! __init__

	#
	#	SCRIPT USAGE
	#

	def prepareGAML():
		print("TODO")
	#!

	def prepareSBatch():
		print("TODO")
	#!

	def runGamaHeadless():
		print("TODO")
	#!

	def runSlurm():
		print("TODO")
	#!

	def genereateCsv():
		print("TODO")
		comokit2png.multithreadCsvProcessing()
		comokit2png.saveToCSV()
	#! genereateCsv

	def genereatePng():
		print("TODO")
		comokit2png.multithreadCsvProcessing()
		comokit2png.saveToCSV()
		col_name = comokit2png.generateColumnName()
		comokit2png.savePngGraphs()
	#!
#! Workspace

class Gama:

	#
	#	BASE
	#
	def __init__(self, pathToHeadlessScript : str, memory : str = "4096m"):
		self.headless = pathToHeadlessScript
		self.memory = memory
	#! __init__

	#
	#	GET/SET
	#
	def getPathToHeadlessScript() -> str:
		return self.pathToHeadlessScript
	def setPathToHeadlessScript(path : str) -> None:
		self.headless = path

	def getMemory() -> str:
		return self.memory
	def setMemory(memory : int) -> None:
		self.memory = memory

	#
	#	SCRIPT USAGE
	#
	
#! Gama

class GamaExploration:

	#
	#	BASE
	#
	
	# Variables
	expSpace : list
	parametersList : list

	# Constructor
	def __init__(self, experimentName : str, gamlFile : str, replication : int, final : int, experimentPerXML : int = "-1", xmlOutputName : str = "headless.xml", until : str = "", seed : int = 0):
		"""
		Constructor for GamaExploration object

		:param experimentName: 		Name of the experiment you want to explore
		:param gamlFile: 			Path to the GAML file to explore
		:param replication: 		Number of replication of each parameter combinaison
		:param final: 				Maximal step to explore (force end the simulation if not already finished)
		:param experimentPerXML: 	(Optional) Split exploration plan in several XML files [Default = disable = -1]
		:param xmlOutputName: 		(Optional) Name of the generated XML file(s) [Default = "headless.xml"]
		:param until: 				(Optional) Define GAML experiment end condition
		:param seed: 				(Optional) Starting seed value [Default = 0]
		
		:return: Workspace object
		"""
		self.experimentName = experimentName
		self.gamlFile = os.path.abspath(gamlFile)
		self.replication = replication
		self.final = final
		self.experimentPerXML = experimentPerXML
		self.xmlOutputName = xmlOutputName
		self.until = until
		self.seed = seed
	#! __init__

	#
	#	GET/SET
	#
	def getExperimentName() -> str:
		return self.experimentName
	def setExperimentName(experimentName : str) -> None:
		self.experimentName = experimentName

	def getGamlFile() -> str:
		return self.gamlFile
	def setGamlFile(gamlFile : str) -> None:
		self.gamlFile = gamlFile

	def getXmlOutputName() -> str:
		return self.xmlOutputName
	def setXmlOutputName(xmlOutputName : str) -> None:
		self.xmlOutputName = xmlOutputName

	def getReplication() -> int:
		return self.replication
	def setReplication() -> None:
		self.replication = replication

	def getExperimentPerXML() -> int:
		return experimentPerXML
	def setExperimentPerXML(experimentPerXML : int) -> None:
		self.experimentPerXML = experimentPerXML

	def getFinal() -> int:
		return self.final
	def setFinal(final: int) -> None:
		self.final = final

	def getUntil() -> str:
		return self.until
	def setUntil(until : str) -> None:
		self.until = until

	def getSeed() -> int:
		return self.seed
	def setSeed(seed : int) -> None:
		self.seed = seed

	def getExperimentSpace() -> list:
		return self.expSpace
	# setExperimentSpace => calcultesExpSpace
	
	def getParametersList() -> list:
		return self.parametersList
	# setParametersList => calcultesExpSpace
	
	#! GET/SET

	#
	#	Functions
	#
	
	def calculatesExperimentSpace() -> None:
		"""
		Scrap experiment's parameters and calculate all the possible combinaison

		Results are store in object's variables [expSpace, parametersList]
		
		:return: None
		"""
		self.expSpace, self.parametersList = generateMultipleXML.generateExperimentUniverse(gamlFilePath)
	#! Functions

#! GamaExploration