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
	def __init__(self, gama : Gama, explorationPlan : GamaExploration, outputDirectory : str):
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
	
	#	=>> VAR <<=
	
	
	def __init__(self):
		print("TODO")
	#!
	
	def setup():
		print("TODO")
	#!

	#
	#	GET/SET
	#

	#
	#	SCRIPT USAGE
	#
	
#! Gama

class GamaExploration:

	#
	#	BASE
	#
	def __init__(self, experimentName : str, gamlFile : str, xmlOutputName : str, replication : int, experimentPerXML : int, final : int, until : str = "", seed : int = 0):
		self.experimentName = experimentName
		self.gamlFile = gamlFile
		self.xmlOutputName = xmlOutputName
		self.replication = replication
		self.experimentPerXML = experimentPerXML
		self.final = final
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
	#! GET/SET

#! GamaExploration