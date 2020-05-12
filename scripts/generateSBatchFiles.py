#!/usr/bin/python3

##################################################
## Python script to generate 
#
## $ python3 generateSBatchFiles.py -h
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMO-TK
## Licence: LGPL 3.0
## Version: 1.0.0
## Maintainer: RoiArthurB
##################################################

import os
import argparse

#
#	VARIABLES
#

xmlPath = ""

#
#	MAIN
#
if __name__ == '__main__':

	# 0 _ Get/Set parameters
	# 
	parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options]')

	#	SBATCH settings
	parser.add_argument('-s', '--submission', metavar='', help="Total of submission on SLURM", default=1, type=int)
	parser.add_argument('-S', '--maxSubmission', metavar='', default=1, type=int, help="Max number of active submission on SLURM")
	parser.add_argument('-n', '--nodes', metavar='', help="Number of nodes to dispatch your exploration on", default=1, type=int)
	parser.add_argument('-T', '--cpuPerTask', metavar='', help="Number of core allocated to a single task", default=1, type=int)
	parser.add_argument('-c', '--core', metavar='', help="Number of cores per node", default=1, type=int)
	parser.add_argument('-t', '--time', metavar='', help="Time (in hour) for your job", default=1, type=int)
	#	GAMA Headless settings
	parser.add_argument('-f', '--folder', metavar='', help="Path to folder where your XML are stored (will gather EVERY! XML file)", type=str, required=True)
	parser.add_argument('-g', '--gama', metavar="", help = 'Path to GAMA headless script (/path/to/your/gama/headless/gama-headless.sh)', type=str, required=False, default="../../GAMA/headless/gama-headless.sh")
	parser.add_argument('-F', '--outputFolder', metavar="", help='Path to folder where GAMA will write simulation\'s console output (default: "/tmp/.gama-output")', type=str, default="/tmp/.gama-output")
	#	Script settings
	parser.add_argument('-o', '--output', metavar="", help='Path to folder where save every needed sbatch files (default: "./sbatchUtilities")', type=str, default="./sbatchUtilities")
	parser.add_argument('--EDF', action='store_true', help='Will add extra parameters for EDF collaboration')

	args = parser.parse_args()

	# 1 _ Setup environment to be sure to launch
	#
	print("=== Prepare everything")
	# Make gama executable
	os.chmod(args.gama, 0o665)

	# Create output folder 
	if not os.path.exists(args.output):
		os.makedirs(args.output)

	# Gather XML in a list
	if args.folder != None:
		if os.path.isdir(args.folder):
			for fname in os.listdir(args.folder)[:1]:
				if fname.endswith('.xml'):
					# Get pattern of xml file before the index element
					xmlPath = os.path.abspath(args.folder + "/" + fname).rsplit("-", 1)[0] + "-"
					break;
			if xmlPath == "":
				raise ValueError('The folder doesn\'t contain any XML file.')
		else: 
			raise ValueError('The folder doesn\'t exist.')
	else:
		raise ValueError('You should specify a folder with XML (w/ `-f`) or an XML (w/ `-x`) in your command.\nTry to launch the script with `-h` for full help options.')

	# 2 _ Create SBatch first script
	#
	print("=== Generate " + args.output + "/sbatch_array.sh file")
	
	sbatchScript = ("#!/bin/bash\n"
		"#-------------------------------------------------------------------------------\n"
		"#\n"
		"# Batch options for SLURM (Simple Linux Utility for Resource Management)\n"
		"# =======================\n"
		"#\n"
		"#SBATCH --array=0-" + str(args.submission -1) + "%" + str(args.maxSubmission) + "\n"
		"#SBATCH --nodes=" + str(args.nodes) + "\n"
		"#SBATCH --cpus-per-task=" + str(args.cpuPerTask) + "\n"
		"#SBATCH --ntasks=" + str(int(args.nodes * args.core / args.cpuPerTask)) + "\n"
		"#SBATCH --ntasks-per-node=" + str(int(args.core / args.cpuPerTask)) + "\n"
		"#SBATCH --time=" + str(args.time) + ":00:00\n"
		"#SBATCH --job-name=COMOKIT\n")
	if (args.EDF):
		sbatchScript += ("#SBATCH --exclusive\n"
				"#SBATCH --partition=cn\n"
				"#SBATCH --wckey=IRD:GAMA\n")
		
	sbatchScript += ("#\n"
			"#-------------------------------------------------------------------------------\n"
			"\n"
			"# Change to submission directory\n"
			"if test -n ${1} ; then cd ${1} ; fi\n"
			"srun --multi-prog vague.cnf\n")

	try:
		file = open(args.output + "/sbatch_array.sh","w")
		file.write( sbatchScript )
		file.close()
	except:
		print("\tError while saving file")
	finally:
		print("\tSaved !")

	# 3 _ Create SBatch second script
	#
	print("=== Generate " + args.output + "/vague.cnf file")

	try:
		file = open(args.output + "/vague.cnf","w")
		file.write( "0-" + str(int(args.nodes * args.core / args.cpuPerTask) - 1 ) + " ./launch_pack_8.sh %t" )
		file.close()
	except:
		print("\tError while saving file")
	finally:
		print("\tSaved !")

	# 4 _ Create gama headless launching script
	#
	print("=== Generate " + args.output + "/launch_pack_8.sh file")

	sbatchGamaScript = ("#!/bin/bash\n"
		"\n"
		"for i in {0.." + str(args.core - 1) + "}\n"
		"do\n"
		"\tid_mask=$(( $1 * " + str(args.core) + " + $i ))\n"
		"\tif [ ! -f  " + xmlPath + "${id_mask}.xml ]; then echo \"le fichier mask-${id_mask}.xml est absent (queue de distrib?)\"; exit 2; fi\n")
	sbatchGamaScript += "\t" + os.path.abspath(args.gama) + " " + xmlPath + "${id_mask}.xml " + os.path.abspath(args.outputFolder) +"\ndone"

	try:
		file = open(args.output + "/launch_pack_8.sh","w")
		file.write( "0-" + str(int(args.nodes * args.core / args.cpuPerTask) - 1 ) + " ./launch_pack_8.sh %t" )
		file.close()
	except:
		print("\tError while saving file")
	finally:
		print("\tSaved !")
