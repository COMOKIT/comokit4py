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

import os, sys, pkgutil
import subprocess, platform, multiprocessing
from . import generateMultipleXML, generateSBatchFiles, comokit2png
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
	processedOutputVariable : dict

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

	def runSlurm(self, log : bool = True, logFileName : str = 'out.log') -> None:
		"""
		Create all needed structures and files to launch SLURM sbatch job

		:param log:			(Optional) Log slurm output in file [Default = True]
		:param logFileName:	(Optional) Name of the log file [Default = 'out.log']

		:return: None
		"""
		if log:
			logfile = open(os.path.join(self.sbatch["outputFolder"], logFileName), 'w')
		
		proc=subprocess.Popen(["slurm", os.path.join(self.sbatch["outputFolder"], 'sbatch_array.sh')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		
		for line in proc.stdout:
			if log:
				logfile.write(line.decode())
			else:
				sys.stdout.write(line.decode())
			proc.wait()
	#!

	#
	#	Generate Output
	def prepareProcessedOutput(self, displayStep : int = 24, median : bool = False, quartile : bool = False, startDate : list[3] = None, startPolicyDate : list[3] = None, endPolicyDate : list[3] = None, cores : int = multiprocessing.cpu_count(), stepTo : int = 1, output_name : list = ["Susceptible", "Recovered", "Presymptomatic", "Asymptomatic", "Symptomatic", "Need hospital", "Need ICU", "Death"], output_color : list = ["g", "b", "olive", "lightgreen", "y", "orange", "r", "m"] ) -> None :
		"""
		"""

		# Auto variables
		self.processedOutputVariable["inputFolder"] = os.path.join(self.workspaceDirectory, "batch_output")
		#self.processedOutputVariable["experimentName"] = self.explorationPlan.getExperimentName()
		self.processedOutputVariable["replication"] = self.explorationPlan.getReplication()

		# Parametrable
		self.processedOutputVariable["displayStep"] = displayStep
		self.processedOutputVariable["median"] = median
		self.processedOutputVariable["quartile"] = quartile
		self.processedOutputVariable["cores"] = cores
		self.processedOutputVariable["stepTo"] = stepTo

		self.processedOutputVariable["output_name"]  = output_name
		self.processedOutputVariable["output_color"] = output_color

		self.processedOutputVariable["startDate"] = startDate
		if startDate != None:
			if endPolicyDate != None:
				self.processedOutputVariable["startPolicyDate"] = startPolicyDate
			if startPolicyDate != None:
				self.processedOutputVariable["endPolicyDate"] = endPolicyDate
	#! prepareProcessedOutput

	def rawOutputProcessing(self) -> list:
		"""
		Compiled COMOKIT's raw output CSV into saveable list

		:return: Python list of post-processed COMOKIT explored data
		"""
		if self.processedOutputVariable == None:
			self.prepareProcessedOutput()
		
		return comokit2png.multithreadCsvProcessing(
			CSV_array = gatheringCSV(batch_path = self.processedOutputVariable["inputFolder"], experimentName = self.explorationPlan.getExperimentName()), 
			output_name = self.processedOutputVariable["output_name"], 
			stepTo = self.processedOutputVariable["stepTo"], 
			replication = self.explorationPlan.getReplication(), 
			cores = self.processedOutputVariable["cores"], 
			quartile = self.processedOutputVariable["quartile"], 
			median = self.processedOutputVariable["median"], 
			variance = False)
	#! rawOutputProcessing

	def generateCsv(self, output : list = None, outputCsvFileName : list = "out") -> bool:
		"""
		Turn COMOKIT's raw output CSV into compiled csv file

		:param output:				(Optional) Output list of raw processed data [Default re-process data]
		:param outputCsvFileName:	(Optional) Name of the png file name (extension automatic) [Default = 'out']

		:return: Bool if csv file saved
		"""
		if output == None:
			output = rawOutputProcessing()

		return comokit2png.saveToCSV(processedCsvArray = output, colName = self.processedOutputVariable["output_name"], csvName = outputCsvFileName)
	#! genereateCsv

	def generatePng(self, title : str = "", outputPngFileName : list = "out", output : list = None) -> bool:
		"""
		Turn COMOKIT's raw output CSV into png graphs

		:param title:				(Optional) Output in png title [Default = ""]
		:param outputPngFileName:	(Optional) Name of the png file name (extension automatic) [Default = 'out']
		:param output:				(Optional) Output list of raw processed data [Default re-process data]

		:return: Bool if png file saved
		"""
		if output == None:
			output = rawOutputProcessing()

		return comokit2png.savePngGraphs(
			output = output, 
			col_name = comokit2png.generateColumnName(quartile = self.processedOutputVariable["quartile"], median = self.processedOutputVariable["median"]), 
			output_color = self.processedOutputVariable["output_color"], 
			outputImgName = outputPngFileName, 
			output_name = self.processedOutputVariable["output_name"],
			displayStep = self.processedOutputVariable["displayStep"], 
			title = title,
			quartile = self.processedOutputVariable["quartile"], 
			median = self.processedOutputVariable["median"], 
			stepTo = self.processedOutputVariable["stepTo"], 
			startDate = self.processedOutputVariable["startDate"], 
			startEpidemyDate = self.processedOutputVariable["startPolicyDate"], 
			endEpidemyDate = self.processedOutputVariable["endPolicyDate"], 
			numberRow = 3, numberCol = 3)
	#! generatePng
	
#! Workspace