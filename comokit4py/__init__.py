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
from . import generateMultipleXML generateSBatchFiles
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
	# setBaseDir => Automatic update from headlessScript
	def getVersion(self) -> str:
		return self.version
	# setVersion => Automatic update from headlessScript
	
#! Gama

class GamaExploration:

	#
	#	BASE
	#
	
	#
	#  Variables
	expSpace : list
	parametersList : list

	def __init__(self, experimentName : str, gamlFile : str, replication : int, final : int, experimentPerXML : int = -1, xmlOutputName : str = "headless.xml", until : str = "", seed : int = 0):
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
	def getExperimentName(self) -> str:
		return self.experimentName
	def setExperimentName(self, experimentName : str) -> None:
		self.experimentName = experimentName

	def getGamlFile(self) -> str:
		return self.gamlFile
	def setGamlFile(self, gamlFile : str) -> None:
		self.gamlFile = gamlFile

	def getXmlOutputName(self) -> str:
		return self.xmlOutputName
	def setXmlOutputName(self, xmlOutputName : str) -> None:
		self.xmlOutputName = xmlOutputName

	def getReplication(self) -> int:
		return self.replication
	def setReplication(self) -> None:
		self.replication = replication

	def getExperimentPerXML(self) -> int:
		return self.experimentPerXML
	def setExperimentPerXML(self, experimentPerXML : int) -> None:
		self.experimentPerXML = experimentPerXML

	def getFinal(self) -> int:
		return self.final
	def setFinal(self, final: int) -> None:
		self.final = final

	def getUntil(self) -> str:
		return self.until
	def setUntil(self, until : str) -> None:
		self.until = until

	def getSeed(self) -> int:
		return self.seed
	def setSeed(self, seed : int) -> None:
		self.seed = seed

	def getExperimentSpace(self) -> list:
		return self.expSpace
	# setExperimentSpace => calcultesExpSpace
	
	def getParametersList(self) -> list:
		return self.parametersList
	# setParametersList => calcultesExpSpace
	
	#! GET/SET

	#
	#	Functions
	#
	def calculatesExperimentSpace(self) -> None:
		"""
		Scrap experiment's parameters and calculate all the possible combinaison

		Results are store in object's variables [expSpace, parametersList]
		
		:return: None
		"""
		self.expSpace, self.parametersList = generateMultipleXML.generateExperimentUniverse(self.gamlFile)
	#! calculatesExperimentSpace
	
	#! Functions

#! GamaExploration

class Workspace:

	#
	#	BASE
	#
	
	#
	# Variables
	edf : bool = False
	sbatch : dict

	def __init__(self, gama : Gama, explorationPlan : GamaExploration, workspaceDirectory : str):
		"""
		Constructor for Workspace object

		:param gama:				Gama object for launching exploration
		:param explorationPlan:		GamaExploration object to know what to launch
		:param workspaceDirectory:	Directory path when everything will be store

		:return: Workspace object
		"""
		self.gama = gama
		self.explorationPlan = explorationPlan
		self.workspaceDirectory = os.path.abspath(workspaceDirectory)
		self.xmlDirectory = os.path.join(self.workspaceDirectory, "xml")
	#! __init__
	
	#
	#	GET/SET
	#
	def getEdfBool(self) -> bool:
		return self.edf
	def setEdfBool(self, edf : bool) -> None:
		self.edf = edf
	def toggleEdfBool(self) -> None:
		self.edf = not self.edf

	#
	#	Functions
	#

	#
	#	Check
	def verifyGama(self) -> bool:
		"""
		Check if GAMA is ready to use in this workspace

		:return: Bool if everything is ready
		"""
		return os.path.isfile( self.gama.getPathToHeadlessScript() ) and is_exe( self.gama.getPathToHeadlessScript() )
	#! verifyGama

	def verifyJavaVersion(self) -> bool:
		"""
		Check if the good Java is installed and usable

		:return: Bool if everything is ready
		"""
		verified = False

		try:
			javaVersion = int(subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode().split('"')[1][2])
			verified = (int(gama.split(".")[1]) <= 6 and javaVersion == 6) or (int(gama.split(".")[1]) > 6 and javaVersion == 8)
		except:
			verified = False

		return verified
	#! verifyJavaVersion

	def verifySlurm(self) -> bool:
		"""
		Check if the slurm is installed and usable

		:return: Bool if everything is ready
		"""
		verified = False

		try:
			verified = subprocess.check_output(['slurm', '-h'], stderr=subprocess.STDOUT).decode() != ""
		except:
			verified = False

		return verified
	#! verifySlurm

	def verifyAll(self, slurm : bool = False) -> bool:
		"""
		Check if everything (GAMA, Java, Slurm?) is installed and usable

		:param slurm: (Optional) Check also for SLURM

		:return: Bool if everything is ready
		"""
		slurmInstalled = True
		if slurm:
			slurmInstalled = self.verifySlurm()
		
		return self.verifyGama() and self.verifyJavaVersion() and slurmInstalled
	#! verifyAll

	#
	#	Generate Input
	def generateNeededForExploration(self) -> None:
		"""
		Create all XML files for running GAMA headless

		:return: None
		"""
		if explorationPlan.expSpace == undefined:
			explorationPlan.ExperimentSpace()

		generateMultipleXML.createXmlFiles(allParamValues = explorationPlan.expSpace, parametersList = explorationPlan.parametersList, xmlFilePath = self.xmlDirectory, replication = explorationPlan.replication, split = explorationPlan.split, output  = os.path.join(self.workspaceDirectory, "batch_output"), seed = explorationPlan.seed, final = explorationPlan.final, until = explorationPlan.until)
	#!generateNeededForExploration

	def prepareSBatch(self, jobTimeout : int, core : int, nodes : int = 1, submission : int = 1, maxSubmission : int = 6, delay : int = 0) -> None:
		"""
		Create all needed structures and files to launch SLURM sbatch job

		:param jobTimeout:		Limit hour for SLURM job
		:param core:			Number of cores used per node
		:param nodes:			(Optional) Number of nodes used by SLURM [Default = 1]
		:param submission:		(Optional) Total of submission on SLURM [Default = 1]
		:param maxSubmission:	(Optional) Max number of active submission on SLURM [Default = 6]
		:param delay:			(Optional) Delay in between launching headless (ex. 2s, 3m, 4h, 5d) [Default = 0]

		:return: None
		"""
		self.sbatch = {
			"output": os.path.join(self.workspaceDirectory, "sbatchUtilities"),
			"outputFolder": os.path.join(self.workspaceDirectory, "sbatchUtilities/tmp/.gama-output")
		}
		# Setup
		xmlPath = generateSBatchFiles.setupGamaEnv(gamaPath = self.gama.getPathToHeadlessScript(), output = self.sbatch["output"], outputFolder = self.sbatch["outputFolder"], absolute = True, folder = self.xmlDirectory )

		# Gen files
		generateSBatchFiles.genSbatchArray(output = self.sbatch["output"], submission = submission, maxSubmission = maxSubmission, nodes = nodes, cpuPerTask = 1, core = core, maxHour = jobTimeout, EDF = self.edf)
		generateSBatchFiles.genVague(output = self.sbatch["output"], nodes = nodes, cpuPerTask = 1, core = core)
		generateSBatchFiles.genLaunchPack(gama = self.gama.getPathToHeadlessScript(), output = self.sbatch["output"], outputFolder = self.sbatch["outputFolder"], xmlPath = self.xmlDirectory, nodes = nodes, cpuPerTask = 1, core = core, delay = delay)
	#!

	#
	#	Run
	def runGamaHeadless(self):
		print("TODO")
	#!

	def runSlurm(self):
		print("TODO")
	#!

	#
	#	Generate Output
	def genereateCsv(self):
		print("TODO")
		comokit2png.multithreadCsvProcessing()
		comokit2png.saveToCSV()
	#! genereateCsv

	def genereatePng(self):
		print("TODO")
		comokit2png.multithreadCsvProcessing()
		comokit2png.saveToCSV()
		col_name = comokit2png.generateColumnName()
		comokit2png.savePngGraphs()
	#!
#! Workspace