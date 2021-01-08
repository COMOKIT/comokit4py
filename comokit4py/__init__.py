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
import subprocess, platform
# Import all other py scripts
__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))

class Gama:

	#
	#	BASE
	#
	
	#
	# Variable
	baseDir : str
	version : str

	def __init__(self, pathToHeadlessScript : str, memory : str = "4096m"):
		self.memory = memory
		self.headless = os.path.abspath(pathToHeadlessScript)
		self.__generateLocalPathVariables()
	#! __init__
	
	#
	#	Private
	#
	def __generateLocalPathVariables(self):
		self.baseDir =  os.path.abspath(os.path.join(self.headless,"../.."))

		# Update path for MacOS
		tempBaseDir = os.path.join(self.baseDir, "Eclipse") if platform.system() != "Linux" else self.baseDir
		self.version = subprocess.check_output(['cat', os.path.join(tempBaseDir, 'configuration/config.ini')], stderr=subprocess.STDOUT).decode().split("version=")[1].split("\n")[0]

	#
	#	GET/SET
	#
	def getPathToHeadlessScript(self) -> str:
		return self.headless
	def setPathToHeadlessScript(self, path : str) -> None:
		self.headless = os.path.abspath(path)
		__generateLocalPathVariables()

	def getMemory(self) -> str:
		return self.memory
	def setMemory(self, memory : int) -> None:
		self.memory = memory

	def getBaseDir(self) -> str:
		return self.baseDir
	#def setBaseDir => Automatic update from headlessScript
	def getVersion(self) -> str:
		return self.version
	#def setVersion => Automatic update from headlessScript

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
		self.workspaceDirectory = os.path.abspath(workspaceDirectory)
	#! __init__

	#
	#	SCRIPT USAGE
	#

	#
	#	Check
	def verifyGama() -> bool:
		return os.path.isfile( self.gama.getPathToHeadlessScript() ) and is_exe( self.gama.getPathToHeadlessScript() )
	#! verifyGama

	def verifyJavaVersion() -> bool:
		javaVersion = int(subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode().split('"')[1][2])

		return (int(gama.split(".")[1]) <= 6 and javaVersion == 6) or (int(gama.split(".")[1]) > 6 and javaVersion == 8)
	#! verifyJavaVersion

	def verifyAll() -> bool:
		return self.verifyGama() and self.verifyJavaVersion()
	#! verifyAll

	#
	#	Generate Input
	def generateNeededForExploration():
		"""
		Function description

		:param A: Desc
		:param B: Desc
		:return: Desc
		"""
		if explorationPlan.expSpace == undefined:
			explorationPlan.ExperimentSpace()

		generateMultipleXML.createXmlFiles(allParamValues = explorationPlan.expSpace, parametersList = explorationPlan.parametersList, xmlFilePath = self.workspaceDirectory, replication = explorationPlan.replication, split = explorationPlan.split, output  = self.workspaceDirectory + "/batch_output", seed = explorationPlan.seed, final = explorationPlan.final, until = explorationPlan.until)
	#!generateNeededForExploration

	def prepareSBatch():
		print("TODO")
	#!

	#
	#	Run
	def runGamaHeadless():
		print("TODO")
	#!

	def runSlurm():
		print("TODO")
	#!

	#
	#	Generate Output
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