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

import os, sys, pkgutil, shutil
import subprocess, platform, multiprocessing
from . import generateMultipleXML, generateSBatchFiles, comokit2png

class Gama:
	"""Gama object

	:param str pathToHeadlessScript:	Gama headless script path
	:param str memory:					(Optinal) Memory of the JVM [Default : "4086m"]
	:param str _baseDir:				(Generated) Base folder of the GAMA software
	:param str _version:				(Generated) Version of the setted GAMA software
	"""
	_baseDir : str
	_version : str

	def __init__(self, pathToHeadlessScript : str, memory : str = "4096m"):
		"""Gama constructor"""

		if pathToHeadlessScript is None:
			gamaHome = os.getenv("GAMA_HOME")
			ext = "bat" if os.name == "nt" else "sh"
			self.headless = os.path.join(gamaHome, "headless", "headless.%s" % ext)
		else:
			self.headless = os.path.abspath(os.path.expanduser(pathToHeadlessScript))

		self.memory = memory
		self.__generateLocalPathVariables()
	#! __init__
	
	#
	#	Private
	#
	def __generateLocalPathVariables(self):
		self._baseDir =  os.path.abspath(os.path.join(self.headless,"../.."))

		# Update path for MacOS
		tempBaseDir = os.path.join(self._baseDir, "Eclipse") if platform.system() != "Linux" else self._baseDir
		self._version = subprocess.check_output(['cat', os.path.join(tempBaseDir, 'configuration/config.ini')], stderr=subprocess.STDOUT).decode().split("version=")[1].split("\n")[0]

	#
	#	GET/SET
	#
	def getPathToHeadlessScript(self) -> str:
		"""Return setted Gama headless script absolute path
		
		:return: Gama headless script absolute path
		"""
		return self.headless
	def setPathToHeadlessScript(self, path : str) -> None:
		"""Set Gama headless script path, and turn it in absolute path

		:param str path: Gama headless script path
		
		:return: None
		"""
		self.headless = os.path.abspath(os.path.expanduser(path))
		__generateLocalPathVariables()

	def getMemory(self) -> str:
		"""Return setted Gama memory JVM
		
		:return: Gama memory JVM
		"""
		return self.memory
	def setMemory(self, memory : str) -> None:
		"""Set Gama memory JVM

		:param str memory: Memory of the JVM (default when created : "4086m")
		
		:return: None
		"""
		self.memory = memory

	def getBaseDir(self) -> str:
		"""Return generated Gama base directory absolute path
		
		:return: Gama base directory absolute path
		"""
		return self._baseDir
	# setBaseDir => Automatic update from headlessScript
	def getVersion(self) -> str:
		"""Return generated Gama version
		
		:return: Gama version
		"""
		return self._version
	# setVersion => Automatic update from headlessScript
	
#! Gama

class GamaExploration:	
	"""GamaExploration object

	Object necessary for defining the exploration.

	:param str experimentName: 		Name of the experiment you want to explore
	:param str gamlFile: 			Path to the GAML file to explore
	:param int replication: 		Number of replication of each parameter combinaison
	:param int final: 				Maximal step to explore (force end the simulation if not already finished)

	:param int experimentPerXML: 	(Optional) Split exploration plan in several XML files [Default = disable = -1]
	:param str xmlOutputName: 		(Optional) Name of the generated XML file(s) [Default = "headless.xml"]
	:param str until: 				(Optional) Define GAML experiment end condition
	:param int seed: 				(Optional) Starting seed value [Default = 0]

	:param list _expSpace:			(Generated) Experiment parameters space
	:param list _parametersList:	(Generated) List of experiment's parameter
	"""
	_expSpace : list
	_parametersList : list

	def __init__(self, experimentName : str, gamlFile : str, replication : int, final : int, experimentPerXML : int = -1, xmlOutputName : str = "headless.xml", until : str = "", seed : int = 0):
		"""Constructor for GamaExploration"""

		self.experimentName = experimentName
		self.gamlFile = os.path.abspath(os.path.expanduser(gamlFile))
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
		"""Return setted GAML experiment name
		
		:return: GAML experiment name
		"""
		return self.experimentName
	def setExperimentName(self, experimentName : str) -> None:
		"""Set GAML experiment name for exploring

		:param str experimentName: GAML experiment name
		
		:return: None
		"""
		self.experimentName = experimentName

	def getGamlFile(self) -> str:
		"""Return setted GAML file
		
		:return: GAML file
		"""
		return self.gamlFile
	def setGamlFile(self, gamlFile : str) -> None:
		"""Set GAML file

		:param str gamlFile: GAML file
		
		:return: None
		"""
		self.gamlFile = gamlFile

	def getXmlOutputName(self) -> str:
		"""Return setted XML name file (used for gama headless)
		
		:return: XML name file
		"""
		return self.xmlOutputName
	def setXmlOutputName(self, xmlOutputName : str) -> None:
		"""Set XML name file (used for gama headless)

		:param str xmlOutputName: XML name file
		
		:return: None
		"""
		self.xmlOutputName = xmlOutputName

	def getReplication(self) -> int:
		"""Return setted replication number
		
		:return: Replication number
		"""
		return self.replication
	def setReplication(self, replication : int) -> None:
		"""Set replication number

		:param int replication: Replication number
		
		:return: None
		"""
		self.replication = replication

	def getExperimentPerXML(self) -> int:
		"""Return setted number of simulation by xml

		.. note::
			This parameter is useful for launching several GAMA in parallel
		
		:return: Simulation per XML number
		"""
		return self.experimentPerXML
	def setExperimentPerXML(self, experimentPerXML : int) -> None:
		"""Set number of simulation by xml

		.. note::
			This parameter is useful for launching several GAMA in parallel

		:param int experimentPerXML: Simulation per XML number
		
		:return: None
		"""
		self.experimentPerXML = experimentPerXML

	def getFinal(self) -> int:
		"""Return setted maximal step for simulations
		
		:return: Max final step
		"""
		return self.final
	def setFinal(self, final: int) -> None:
		"""Set maximal step for simulations

		:param int final: Max final step
		
		:return: None
		"""
		self.final = final

	def getUntil(self) -> str:
		"""Return setted simulation stop condition
		
		:return: Stop condition
		"""
		return self.until
	def setUntil(self, until : str) -> None:
		"""Set simulation stop condition

		:param str final: Stop condition
		
		:return: None
		"""
		self.until = until

	def getSeed(self) -> int:
		"""Return setted starting seed
		
		:return: Seed
		"""
		return self.seed
	def setSeed(self, seed : int) -> None:
		"""Set starting seed

		:param str seed: Start seed value
		
		:return: None
		"""
		self.seed = seed

	def getExperimentSpace(self) -> list:
		"""Return generated experiment space parameters (full combinaison set)

		.. warning::
			This parameter is automatically setted by the ``self.calculatesExperimentSpace()`` function
		
		:return: list
		"""
		return self._expSpace
	# setExperimentSpace => calcultesExpSpace
	
	def getParametersList(self) -> list:
		"""Return generated experiment parameters list

		.. warning::
			This parameter is automatically setted by the ``self.calculatesExperimentSpace()`` function
		
		:return: list
		"""
		return self._parametersList
	# setParametersList => calcultesExpSpace
	
	#! GET/SET

	#
	#	Functions
	#
	def calculatesExperimentSpace(self) -> None:
		"""Scrap experiment's parameters and calculate all the possible combinaison

		Results are store in object's variables [expSpace, parametersList]
		
		:return: None
		"""
		self._expSpace, self._parametersList = generateMultipleXML.generateExperimentUniverse(self.gamlFile, self.experimentName)
	#! calculatesExperimentSpace

#! GamaExploration

class Workspace:
	"""
	Constructor for Workspace object

	:param Gama gama:						Gama object for launching exploration
	:param GamaExploration explorationPlan:	GamaExploration object to know what to launch
	:param str workspaceDirectory:			Directory path when everything will be store
	:param bool _edf:						(Optional) toto
	:param dict _sbatch:					(Generated) toto
	:param dict _processedOutputVariable:	(Generated) toto

	:return: Workspace object
	"""
	_edf : bool = False
	_sbatch : dict
	_processedOutputVariable : dict = {}

	def __init__(self, gama : Gama, explorationPlan : GamaExploration, workspaceDirectory : str, rebuildWorkspace : bool = False):
		"""
		Constructor for Workspace object

		:param Gama gama:						Gama object for launching exploration
		:param GamaExploration explorationPlan:	GamaExploration object to know what to launch
		:param str workspaceDirectory:			Directory path when everything will be store
		:param bool rebuildWorkspace:			(Optional) Destroy and rebuild folder architecture [Default: False]

		:return: Workspace object
		"""
		self.gama = gama
		self.explorationPlan = explorationPlan
		self.workspaceDirectory = os.path.abspath(os.path.expanduser(workspaceDirectory))
		if not os.path.exists( self.workspaceDirectory ):
			os.mkdir( self.workspaceDirectory )

		self.xmlDirectory = os.path.join(self.workspaceDirectory, "xml")

		if rebuildWorkspace:
			self.rebuildWorkspace()
	#! __init__
	
	#
	#	GET/SET
	#
	def getEdfBool(self) -> bool:
		return self._edf
	def setEdfBool(self, edf : bool) -> None:
		self._edf = edf
	def toggleEdfBool(self) -> None:
		self._edf = not self._edf

	#
	#	Functions
	#
	def rebuildWorkspace(self) -> None:
		"""Destroy and rebuild folder architecture

		:return: None
		"""
		if  os.path.exists( self.workspaceDirectory ):
			shutil.rmtree( self.workspaceDirectory )
		os.mkdir( self.workspaceDirectory )

		if  os.path.exists( self.workspaceDirectory ):
			shutil.rmtree( self.workspaceDirectory )
		os.mkdir( self.workspaceDirectory )

		if  os.path.exists( self.xmlDirectory ):
			shutil.rmtree( self.xmlDirectory )
		os.mkdir( self.xmlDirectory )
	#! rebuildWorkspace


	#
	#	Check
	def verifyGama(self) -> bool:
		"""Check if GAMA is ready to use in this workspace

		:return: Bool if everything is ready
		"""
		return os.path.isfile( self.gama.getPathToHeadlessScript() ) and os.access(self.gama.getPathToHeadlessScript(), os.X_OK)
	#! verifyGama

	def verifyJavaVersion(self) -> bool:
		"""Check if the good Java is installed and usable

		:return: Bool if everything is ready
		"""
		verified = False

		try:
			javaVersion = int(subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode().split('"')[1][2])
			verified = (int(self.gama.getVersion().split(".")[1]) <= 6 and javaVersion == 6) or (int(self.gama.getVersion().split(".")[1]) > 6 and javaVersion == 8)
		except:
			verified = False

		return verified
	#! verifyJavaVersion

	def verifySlurm(self) -> bool:
		"""Check if the slurm is installed and usable

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
		"""Check if everything (GAMA, Java, Slurm?) is installed and usable

		:param bool slurm: (Optional) Check also for SLURM

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
		"""Create all XML files for running GAMA headless

		:return: None
		"""
		if not hasattr(self.explorationPlan, '_expSpace'):
			self.explorationPlan.calculatesExperimentSpace()

		if not os.path.exists( self.xmlDirectory ):
			os.mkdir( self.xmlDirectory )

		generateMultipleXML.createXmlFiles(
			experimentName = self.explorationPlan.getExperimentName(),
			gamlFilePath = self.explorationPlan.getGamlFile(),
			allParamValues = self.explorationPlan.getExperimentSpace(), 
			parametersList = self.explorationPlan.getParametersList(), 
			xmlFilePath = os.path.join(self.xmlDirectory, "headless.xml"), 
			replication = self.explorationPlan.getReplication(), 
			split = self.explorationPlan.getExperimentPerXML(), 
			output  = os.path.join(self.workspaceDirectory, "batch_output"), 
			seed = self.explorationPlan.getSeed(), 
			final = self.explorationPlan.getFinal(), 
			until = self.explorationPlan.getUntil()
		)
	#!generateNeededForExploration

	def prepareSBatch(self, jobTimeout : int, core : int, nodes : int = 1, submission : int = 1, maxSubmission : int = 6, delay : int = 0) -> None:
		"""Create all needed structures and files to launch SLURM sbatch job

		:param int jobTimeout:		Limit hour for SLURM job
		:param int core:			Number of cores used per node
		:param int nodes:			(Optional) Number of nodes used by SLURM [Default = 1]
		:param int submission:		(Optional) Total of submission on SLURM [Default = 1]
		:param int maxSubmission:	(Optional) Max number of active submission on SLURM [Default = 6]
		:param int delay:			(Optional) Delay in between launching headless (ex. 2s, 3m, 4h, 5d) [Default = 0]

		:return: None
		"""
		self._sbatch = {
			"output": os.path.join(self.workspaceDirectory, "sbatchUtilities"),
			"outputFolder": os.path.join(self.workspaceDirectory, "sbatchUtilities/tmp/.gama-output")
		}
		# Setup
		xmlPath = generateSBatchFiles.setupGamaEnv(
			gamaPath = self.gama.getPathToHeadlessScript(), 
			output = self._sbatch["output"], 
			outputFolder = self._sbatch["outputFolder"], 
			absolute = True, 
			folder = self.xmlDirectory
		)

		# Gen files
		generateSBatchFiles.genSbatchArray(
			output = self._sbatch["output"], 
			submission = submission, 
			maxSubmission = maxSubmission, 
			nodes = nodes, 
			cpuPerTask = 1, 
			core = core, 
			maxHour = jobTimeout, 
			EDF = self._edf
		)
		generateSBatchFiles.genVague(
			output = self._sbatch["output"], 
			nodes = nodes, 
			cpuPerTask = 1, 
			core = core
		)
		generateSBatchFiles.genLaunchPack(
			gama = self.gama.getPathToHeadlessScript(), 
			output = self._sbatch["output"],
			outputFolder = self._sbatch["outputFolder"], 
			xmlPath = self.xmlDirectory, 
			nodes = nodes, 
			cpuPerTask = 1, 
			core = core, 
			delay = delay
		)
	#! prepareSBatch

	#
	#	Run
	def __runExplo(self, command : list, log : bool, logFileName : str) -> None:
		"""Create all needed structures and files to launch SLURM sbatch job

		:param list command:	Command to launch splitted by space
		:param bool log:		(Optional) Log std output in file [Default = True]
		:param str logFileName:	(Optional) Name of the log file [Default = 'out.log']

		:return: None
		"""
		if log:
			if not os.path.exists( self.workspaceDirectory ):
				os.mkdir( self.workspaceDirectory )

			logfile = open(os.path.join(self.workspaceDirectory, logFileName), 'w')
		
		proc=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		
		for line in proc.stdout:
			if log:
				logfile.write(line.decode())
			else:
				sys.stdout.write(line.decode())
			proc.wait()
	#! __runExplo

	def runGamaHeadless(self, log : bool = True, logFileName : str = 'out.log', cores : int = 1) -> None:
		"""Create all needed structures and files to launch SLURM sbatch job

		:param bool log:		(Optional) Log slurm output in file [Default = True]
		:param str logFileName:	(Optional) Name of the log file [Default = 'out.log']
		:param int core:		(Optional) Number of cores allowed to GAMA [Default = 1]

		:return: None
		"""

		xmlFiles = [f for f in os.listdir(self.xmlDirectory) if os.path.isfile(os.path.join(self.xmlDirectory, f)) and (".xml" in f)]

		for xml in xmlFiles:
			xml = os.path.join(self.xmlDirectory, xml)

			self.__runExplo(
				command = [self.gama.getPathToHeadlessScript(), "-m", str(self.gama.getMemory()), "-hpc", str(cores), xml, self.workspaceDirectory], 
				log = log, 
				logFileName = logFileName
			)
	#! runGamaHeadless

	def runSlurm(self, log : bool = True, logFileName : str = 'out.log') -> None:
		"""Create all needed structures and files to launch SLURM sbatch job

		:param bool log:		(Optional) Log slurm output in file [Default = True]
		:param str logFileName:	(Optional) Name of the log file [Default = 'out.log']

		:return: None
		"""
		self.__runExplo(
			command = ["slurm", os.path.join(self._sbatch["outputFolder"], 'sbatch_array.sh')], 
			log = log, 
			logFileName = logFileName
		)
	#! runSlurm

	#
	#	Generate Output
	def prepareProcessedOutput(self, displayStep : int = 24, median : bool = False, quartile : bool = False, startDate : list = None, startPolicyDate : list = None, endPolicyDate : list = None, cores : int = multiprocessing.cpu_count(), stepTo : int = 1, output_name : list = ["Susceptible", "Recovered", "Presymptomatic", "Asymptomatic", "Symptomatic", "Need hospital", "Need ICU", "Death"], output_color : list = ["g", "b", "olive", "lightgreen", "y", "orange", "r", "m"] ) -> None :
		"""Prepare private variables for following functions generating CSV or PNG output files

		:param int displayStep:			(Optional) Output list of raw processed data [Default re-process data]
		:param bool median:				(Optional) Display median curve in graph [Default False]
		:param bool quartile:			(Optional) Display quartile curves in graph (override median option) [Default False]
		:param list[3] startDate:		(Optional) Set starting real date in PNG x axis [Default None]
		:param list[3] startPolicyDate:	(Optional) Set starting policy grey area in PNG (needs startDate and endPolicyDate) [Default None]
		:param list[3] endPolicyDate:	(Optional) Set starting policy grey area in PNG (needs --startDate and --startPolicy) [Default toto]
		:param int cores:				(Optional) Number of core to use [Default Max number of cores available]
		:param int stepTo:				(Optional) Compile several steps in one [Default 1 => Disable]
		:param list output_name:		(Optional) List of outputed graphs [Default ["Susceptible", "Recovered", "Presymptomatic", "Asymptomatic", "Symptomatic", "Need hospital", "Need ICU", "Death"] ]
		:param list output_color:		(Optional) Colors of outputed graphs [Default ["g", "b", "olive", "lightgreen", "y", "orange", "r", "m"]]

		.. warning::
			Date parameter should follow this form : ``[YYYY, MM, DD]`` (list of int)
			
			⚠️ Changing value of ``output_name`` and ``output_color`` may break following ``self.generateCsv()`` and ``self.generatePng()`` functions ⚠️

		:return: None
		"""

		# Auto variables
		self._processedOutputVariable["inputFolder"] = os.path.join(self.workspaceDirectory, "batch_output")
		#self._processedOutputVariable["experimentName"] = self.explorationPlan.getExperimentName()
		self._processedOutputVariable["replication"] = self.explorationPlan.getReplication()

		# Parametrable
		self._processedOutputVariable["displayStep"] = displayStep
		self._processedOutputVariable["median"] = median
		self._processedOutputVariable["quartile"] = quartile
		self._processedOutputVariable["cores"] = cores
		self._processedOutputVariable["stepTo"] = stepTo
		self._processedOutputVariable["output_name"]  = output_name
		self._processedOutputVariable["output_color"] = output_color

		self._processedOutputVariable["startDate"] = startDate
		if startDate != None:
			if endPolicyDate != None:
				self._processedOutputVariable["startPolicyDate"] = startPolicyDate
			if startPolicyDate != None:
				self._processedOutputVariable["endPolicyDate"] = endPolicyDate
	#! prepareProcessedOutput

	def rawOutputProcessing(self) -> list:
		"""Compiled COMOKIT's raw output CSV into saveable list

		:return: Python list of post-processed COMOKIT explored data
		"""
		if self._processedOutputVariable == None:
			self.prepareProcessedOutput()
		
		return comokit2png.multithreadCsvProcessing(
			CSV_array = comokit2png.gatheringCSV(
				batch_path = self._processedOutputVariable["inputFolder"], 
				experimentName = self.explorationPlan.getExperimentName()
			), 
			output_name = self._processedOutputVariable["output_name"], 
			stepTo = self._processedOutputVariable["stepTo"], 
			replication = self.explorationPlan.getReplication(), 
			cores = self._processedOutputVariable["cores"], 
			quartile = self._processedOutputVariable["quartile"], 
			median = self._processedOutputVariable["median"], 
			variance = False
		)
	#! rawOutputProcessing

	def generateCsv(self, output : list = None, outputCsvFileName : str = "out") -> bool:
		"""Turn COMOKIT's raw output CSV into compiled csv file

		:param list output:				(Optional) Output list of raw processed data [Default re-process data]
		:param str outputCsvFileName:	(Optional) Name of the png file name (extension automatic) [Default = 'out']

		:return: Bool if csv file saved
		"""
		if output == None:
			output = rawOutputProcessing()

		return comokit2png.saveToCSV(
			processedCsvArray = output, 
			colName = self._processedOutputVariable["output_name"], 
			csvName = outputCsvFileName
		)
	#! genereateCsv

	def generatePng(self, title : str = "", output : list = None, outputPngFileName : list = "out") -> bool:
		"""Turn COMOKIT's raw output CSV into a png graphs

		:param str title:				(Optional) Output in png title [Default Disable]
		:param list output:				(Optional) Output list of raw processed data [Default re-process data]
		:param list outputPngFileName:	(Optional) Name of the png file name (extension automatic) [Default = 'out']

		:return: Bool if png file saved
		"""
		if output == None:
			output = rawOutputProcessing()

		return comokit2png.savePngGraphs(
			output = output, 
			col_name = comokit2png.generateColumnName(
				quartile = self._processedOutputVariable["quartile"], 
				median = self._processedOutputVariable["median"]
			), 
			output_color = self._processedOutputVariable["output_color"], 
			outputImgName = outputPngFileName, 
			output_name = self._processedOutputVariable["output_name"],
			displayStep = self._processedOutputVariable["displayStep"], 
			title = title,
			quartile = self._processedOutputVariable["quartile"], 
			median = self._processedOutputVariable["median"], 
			stepTo = self._processedOutputVariable["stepTo"], 
			startDate = self._processedOutputVariable["startDate"], 
			startEpidemyDate = self._processedOutputVariable["startPolicyDate"], 
			endEpidemyDate = self._processedOutputVariable["endPolicyDate"], 
			numberRow = 3, 
			numberCol = 3
		)
	#! generatePng

#! Workspace
