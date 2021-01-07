import os, pkgutil
__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))

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

class exploration:

	#
	#	BASE
	#
	
	gama : Gama 

	def __init__():
		print("TODO")
	#!

	#
	#	GET/SET
	#

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

	#def 