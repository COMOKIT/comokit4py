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

import os
import argparse

#
#	VARIABLES
#

xmlList = []

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
	parser.add_argument('-f', '--folder', metavar='', help="Path to folder where your XML are stored (will gather EVERY! XML file)", type=str, required=False)
	parser.add_argument('-x', '--xml', metavar="", help = 'Path to your XML (/path/to/your/headlessExplo.xml)', type=str, required=False)
	parser.add_argument('-g', '--gama', metavar="", help = 'Path to GAMA headless script (/path/to/your/gama/headless/gama-headless.sh)', type=str, required=True)
	parser.add_argument('-F', '--outputFolder', metavar="", help='Path to folder where GAMA will write simulation\'s console output', type=str, default="./.gama-output")
	#	Script settings
	parser.add_argument('-o', '--output', metavar="", help='Path to your saved conf file (default: "./gama-headless.conf")', type=str, default="./gama-headless.conf")

	#parser.add_argument('-xml', metavar=("<experiment name>", "/path/to/file.gaml", "/path/to/file.xml"), nargs = 3, help = 'Classical xml arguments', required=False)
	args = parser.parse_args()

	# 1 _ Setup environment to be sure to launch
	#
	print("=== Prepare everything")
	# Make gama executable
	os.chmod(args.gama, 0o665)

	# Gather XML in a list
	if args.folder != None:
		if os.path.isdir(args.folder):
			for fname in os.listdir(args.folder):
				if fname.endswith('.xml'):
					xmlList.append(args.folder + "/" + fname)
			if len(xmlList) == 0:
				raise ValueError('The folder doesn\'t contain any XML file.')
		else: 
			raise ValueError('The folder doesn\'t exist.')
	elif args.xml != None:
		if os.path.isfile(args.xml) and args.xml.endswith('.xml'):
			xmlList.append(args.xml)
		else: 
			raise ValueError('The XML file do not exist or is not an XML file.')
	else:
		raise ValueError('You should specify a folder with XML (w/ `-f`) or an XML (w/ `-x`) in your command.\nTry to launch the script with `-h` for full help options.')

	# 2 _ Create conf file
	#
	print("=== Generate " + args.output + " file")
	file = open(args.output,"w") 

	for i in range(len(xmlList)):
		file.write( str(i) + " " + os.path.abspath(args.gama) + " " + xmlList[i] + " " + os.path.abspath(args.outputFolder) + "\n" )
	 
	file.close() 

	# 3 _ Create SLURM Command(s)
	#
	print("=== Generate SLURM command")
	print("srun --wckey=ird:gama -n " + str(args.core) + " --partition=cn -J COMOKIT --exclusive -N " + str(args.node) + " ----ntasks-per-node=" + str(args.core) + " --time 420 -o log.txt --comment COMOKIT --multi-prog gama-headless.conf &")

	# 4 _ Done
	#
	print("\n=== Done ;)")