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
	parser.add_argument('-d', '--delay', metavar='', help="Delay in between launching headless (ex. 2s, 3m, 4h, 5d)", required=False)
	#	GAMA Headless settings
	parser.add_argument('-f', '--folder', metavar='', help="Path to folder where your XML are stored (will gather EVERY! XML file)", type=str, required=True)
	parser.add_argument('-g', '--gama', metavar="", help = 'Path to GAMA headless script (/path/to/your/gama/headless/gama-headless.sh)', type=str, required=False, default="../../GAMA/headless/gama-headless.sh")
	parser.add_argument('-F', '--outputFolder', metavar="", help='Path to folder where GAMA will write simulation\'s console output (default: "./sbatchUtilities/tmp/.gama-output")', type=str, default="./sbatchUtilities/tmp/.gama-output")
	#	Script settings
	parser.add_argument('-o', '--output', metavar="", help='Path to folder where save every needed sbatch files (default: "./sbatchUtilities")', type=str, default="./sbatchUtilities")
	parser.add_argument('--EDF', action='store_true', help='Will add extra parameters for EDF collaboration')
	parser.add_argument('-A', action='store_true', help='Will turn every path in absolute path')

	args = parser.parse_args()

	# 1 _ Setup environment to be sure to launch
	#
	print("=== Prepare everything")
	# Make gama executable
	os.chmod(args.gama, 0o555)

	# Create output folder 
	if not os.path.exists(args.output):
		os.makedirs(args.output)

	# Set absolute path or not
	if args.A:
		args.output = os.path.abspath(args.output)
		args.gama = os.path.abspath(args.gama)
		args.outputFolder = os.path.abspath(args.outputFolder)

	# Gather XML in a list
	if args.folder != None:
		if os.path.isdir(args.folder):
			for fname in os.listdir(args.folder)[:1]:
				if fname.endswith('.xml'):
					# Get pattern of xml file before the index element
					xmlPath = (os.path.abspath(args.folder + "/" + fname).rsplit("-", 1)[0] + "-") if args.A else ((args.folder + "/" + fname).rsplit("-", 1)[0] + "-")
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
			"srun --multi-prog " +  args.output + "/vague.cnf\n")

	try:
		file = open(args.output + "/sbatch_array.sh","w")
		file.write( sbatchScript )
		file.close()
		os.chmod(args.output + "/sbatch_array.sh", 0o775)
	except:
		print("\tError while saving file")
	finally:
		print("\tSaved !")

	# 3 _ Create SBatch second script
	#
	print("=== Generate " + args.output + "/vague.cnf file")

	try:
		file = open(args.output + "/vague.cnf","w")
		file.write( "0-" + str(int(args.nodes * args.core / args.cpuPerTask) - 1 ) + " " + args.output + "/launch_pack_8.sh %t" )
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
		"id_mask=$(( $SLURM_ARRAY_TASK_ID * " + str(int(args.nodes * args.core / args.cpuPerTask)) + " + $1 ))\n"
		"if [ ! -f  " + xmlPath + "${id_mask}.xml ]; then echo \"le fichier mask-${id_mask}.xml est absent (queue de distrib?)\"; exit 2; fi\n")
	sbatchGamaScript += args.gama + " -hpc 1 " + xmlPath + "${id_mask}.xml " + args.outputFolder+"${id_mask}"

	if args.delay != None:
		sbatchGamaScript += "\nsleep "+args.delay

	try:
		file = open(args.output + "/launch_pack_8.sh","w")
		file.write( sbatchGamaScript )
		file.close()
		os.chmod(args.output + "/launch_pack_8.sh", 0o775)
	except:
		print("\tError while saving file")
	finally:
		print("\tSaved !")
