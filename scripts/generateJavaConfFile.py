#!/usr/bin/python3

##################################################
## Python script to generate .conf to launch batch exploration of COMOKIT on an SLURM HPC
## To use it you should write it like so :
#
## $ python3 generateJavaConfFile.py numberOfLine /path/to/file.xml /path/to/output.conf (optional)/path/to/gama.jar (optional)/path/to/batchOutputFolder
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMO-TK
## Licence: LGPL 3.0
## Version: 0.0.1
## Maintainer: RoiArthurB
##################################################

import sys
import argparse

#
#	VARIABLES
#

pathToJar = "D:/Downloads/a/gama-headless1.8.jar"
batchOutputFolder = "D:/Downloads/a/"

#
#	MAIN
#
if __name__ == '__main__':

	# 0 _ Get/Set parameters
	# 
	parser = argparse.ArgumentParser()
	#	SLURM settings
	parser.add_argument('-n', '--node', metavar='', help="Number of nodes to dispatch your exploration on", default=1, type=int)
	parser.add_argument('-c', '--core', metavar='', help="Number of cores per node", default=-1, type=int)
	#	GAMA Headless settings
	parser.add_argument('-f', '--folder', metavar='', help="Absolute path to folder where your XML are stored (will gather EVERY! XML file)", type=str, required=False)
	parser.add_argument('-x', '--xml', metavar="", help = 'Absolute path to your XML (/path/to/your/headlessExplo.xml)', type=str, required=False)
	parser.add_argument('-g', '--gama', metavar="", help = 'Absolute path to GAMA headless script (/path/to/your/gama/headless/gama-headless.sh)', type=str, required=True)
	#	Script settings
	parser.add_argument('-o', '--output', metavar="", help='Path to your saved conf file (default: "./gama-headless.conf")', type=str, default="./gama-headless.conf")

	#parser.add_argument('-xml', metavar=("<experiment name>", "/path/to/file.gaml", "/path/to/file.xml"), nargs = 3, help = 'Classical xml arguments', required=False)
	args = parser.parse_args()