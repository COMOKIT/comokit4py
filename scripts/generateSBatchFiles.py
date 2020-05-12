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

xmlList = []

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
	parser.add_argument('-f', '--folder', metavar='', help="Path to folder where your XML are stored (will gather EVERY! XML file)", type=str, required=False)
	parser.add_argument('-x', '--xml', metavar="", help = 'Path to your XML (/path/to/your/headlessExplo.xml)', type=str, required=False)
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
			for fname in os.listdir(args.folder)[::-1]:
				if fname.endswith('.xml'):
					xmlList.append( os.path.abspath(args.folder + "/" + fname) )
			if len(xmlList) == 0:
				raise ValueError('The folder doesn\'t contain any XML file.')
		else: 
			raise ValueError('The folder doesn\'t exist.')
	elif args.xml != None:
		if os.path.isfile(args.xml) and args.xml.endswith('.xml'):
			xmlList.append( os.path.abspath(args.xml) )
		else: 
			raise ValueError('The XML file do not exist or is not an XML file.')
	else:
		raise ValueError('You should specify a folder with XML (w/ `-f`) or an XML (w/ `-x`) in your command.\nTry to launch the script with `-h` for full help options.')

	# 2 _ Create SBatch first script
	#
	"""
	#!/bin/bash
	#-------------------------------------------------------------------------------
	#
	# Batch options for SLURM (Simple Linux Utility for Resource Management)
	# =======================
	#
	#SBATCH --array=0-26%6         #A lancement de 27 soumission slurm avec au maximum 6 soumission actives ( soit 96 noeuds si 16 noeuds par soumission)
	#SBATCH --nodes=16              #B allocation de 16 noeuds par soumission
	#SBATCH --cpus-per-task=1      #C on fixe le java sur un coeur. on pourrait tester avec 2 mais apres
	#SBATCH --ntasks=576            #D  nombre de tache slurm (nombre d'instannce java) = B * 36 ( nombre de couer par noeud) / C            
	#SBATCH --ntasks-per-node=36   #E nombre de cpu par noeud / C
	#SBATCH --exclusive
	#SBATCH --time=1:00:00
	#SBATCH --partition=cn
	#SBATCH --job-name=COMOKIT
	#SBATCH --wckey=IRD:GAMA
	#
	#-------------------------------------------------------------------------------

	# Change to submission directory
	if test -n "$SLURM_SUBMIT_DIR" ; then cd $SLURM_SUBMIT_DIR ; fi
	srun --multi-prog vague.cnf
	"""