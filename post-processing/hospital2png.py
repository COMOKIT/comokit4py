#!/usr/bin/python3

##################################################
## Python script to generate PNG graphs from aggregated hospital's COMOKIT exploration
## To use it you should write it like so :
#
## $ python3 hospital2png.py [-h]
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMOKIT-HPC
## Licence: LGPL 3.0
## Maintainer: RoiArthurB
##################################################

from os import listdir
from os.path import isfile, join
import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 0 _ Get/Set parameters
#
parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options]')

# Files
parser.add_argument('-i', '--inputFolder', metavar="", help='Path to folder where are saved all the COMOKIT CSV files from explorations (default: "./batch_output")', type=str, default="./batch_output")
parser.add_argument('-o', '--outputImg', metavar="", help='Where to save output graph (default: "./out" =generate=> "./out[GeneratedNumber].png")', type=str, default="./out")
parser.add_argument('-e', '--experimentName', metavar="", help='Name of the experiment (if you have several in a same folder)', type=str, default="")
parser.add_argument('-idx', '--indexColumn', metavar="", help='The indexes of column to be aggregated and plot (default: [all])', nargs="+", type=int, default="")

# PNG
parser.add_argument('-t', '--title', metavar="", help='Graph title (default: [disabled])', type=str, default="")

# Other
parser.add_argument('-q', '--quiet', action='store_true', help='Disable verbose mode')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable extra verbose')

args = parser.parse_args()

# 1 _ Gathering COMOKIT datasets
#

# Get all CSV files
batch_path = args.inputFolder
onlyfiles = [f for f in listdir(batch_path) if isfile(join(batch_path, f))
	and (("batchAggregated-" + args.experimentName in f) or ("Hospital_stats-"  + args.experimentName in f))]

if args.verbose:
	print("Gathering " + str(len(onlyfiles)) + " CSV files")

# Use dictionnary to keep col name and collect per col
dictionaryCSVs = {}

# Gather all CSV data for post processing
for csv_file in onlyfiles:

	df = pd.read_csv(join(batch_path, csv_file), dtype="float").reset_index(drop=True)
	df_key = df
	if args.indexColumn:
		df_key = df.iloc[:,args.indexColumn]

	# Create directory entries on first loop
	if len(dictionaryCSVs) == 0:
			for key in df_key:
				dictionaryCSVs[key] = []

	# Gather data
	for key in df_key:
		dictionaryCSVs[key].append(df[key][0])

if args.verbose:
	print("=== End gathering CSVs ===")

# Transform dictionnary to list
CSVs = []
for key, value in dictionaryCSVs.items():
    CSVs.append(value[:])

# 2 _ Create graph
#

fig, ax = plt.subplots()
fig.suptitle( args.title )

# Plot all whiskers boxes
ax.boxplot(CSVs)

# Change index name
# > Add 1 empty element to debug origin tick
plt.xticks(np.arange(len(dictionaryCSVs)+1), [""] + list(dictionaryCSVs.keys()))
fig.autofmt_xdate(rotation=25)

# Save output graph
plt.tight_layout()
plt.savefig(args.outputImg + '.png', bbox_inches='tight')

if not args.quiet:
    print("Output image saved as : " + args.outputImg + '.png')
