#!/usr/bin/python3

##################################################
## Python script to split badly concat CSV files
## To use it you should write it like so :
#
## $ python3 generateJavaConfFile.py -h
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMOKIT-HPC
## Licence: LGPL 3.0
## Version: 1.0.0
## Maintainer: RoiArthurB
##################################################

import os
import argparse


def newFileWithUniqueId( fileName ):
	newId = 0

	# Extract file name schema
	nFileName = os.path.join( args.folder, "batchDetailed-" + str(newId) + "_" + fileName.split("_")[1] )

	# Search un-use file name
	while os.path.exists( nFileName ):
		newId = newId + 1
		nFileName = os.path.join( args.folder, "batchDetailed-" + str(newId) + "_" + fileName.split("_")[1] )

	return nFileName


textFirstLine = ""

# 0 _ Get/Set parameters
# 
parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options]')
#	SLURM settings
parser.add_argument('-F', '--folder', metavar='', help="Folder from where scrapping CSV files", default=1, type=str)
args = parser.parse_args()

onlyfiles = [f for f in os.listdir(args.folder) if os.path.isfile(os.path.join(args.folder, f))]

fWithMultipleCSV = []

# List all CSV with multiple ones
for f in onlyfiles:
	with open( os.path.join(args.folder, f), "r" ) as file:
		oldFirstCol = 0
		firstLine = True

		rows = file.readlines()
		for row in rows:

			if firstLine:
				firstLine = False
				continue

			if int(row.split(",")[0]) < oldFirstCol:
				fWithMultipleCSV.append(f)

		rows = file.readlines()
		for row in rows:

			if firstLine:
				textFirstLine = row
				firstLine = False
				continue

			firstCol = row.split(",")[0]

			if int(firstCol) < oldFirstCol:
				print("Merde !")
				print(f)
			
			oldFirstCol = int(firstCol)