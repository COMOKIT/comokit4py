#!/usr/bin/python3

##################################################
## Python script to generate heatmaps
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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

# 0 _ Get/Set parameters
# 
parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options]')
# CSV
parser.add_argument('-f', '--folder', metavar='', help="Folder from where scrapping CSV files", default="./", type=str)
parser.add_argument('-e', '--exclude', metavar='', help="List of variable to exclude", nargs='+', type=str)
# PNG
parser.add_argument('-t', '--title', metavar='', help="Graph title", default="", type=str)
parser.add_argument('-o', '--output', metavar='', help="Path and name of the output file [Default = './out']", default="./out", type=str)
parser.add_argument('--csv', action='store_true', help='Save output as CSV file')
# Script
parser.add_argument('-m', '--mode', metavar='', help="[1: Final death number, 2: Last day death]", type=int, required=True)
parser.add_argument('-q', '--quiet', action='store_true', help='Disable verbose')
args = parser.parse_args()

## Jupyter notebook CLI parameters
#
#args.folder = "/tmp/HeadlessComparison"
#args.exclude = ["allow_transmission_building"]
#


# 1 _ Scrap CSV
# 
onlyfiles = [f for f in os.listdir(args.folder) if os.path.isfile(os.path.join(args.folder, f)) and ("csv" in f)]

if not args.quiet:
    print("Scrapped", len(onlyfiles), "csv files")


# 2 _ Make DataFrame
# 

heatmap = pd.DataFrame()
# Used in png
label = {"x": "-1", "y": "-1"}

for CSV in onlyfiles:
    col = index = -1
    variableExcluded = 0
    # Check and create col/row in dataframe
    for i in range(len(CSV.split("-"))):
        val = CSV.split("-")[i].rsplit("_",1)
        
        # Eclude parameters from heatmap
        if val[0] in args.exclude:
            variableExcluded = variableExcluded +1
            continue
        else:
            val=val[1].split(".csv")[0]
        
        # Add col
        if (i == variableExcluded):
            col = val
            if not (val in heatmap.columns):
                heatmap[val]=np.nan
                # Set col variable name
                if label["x"] == "-1":
                    label["x"] = CSV.split("-")[i].rsplit("_",1)[0]
        
        # Add row
        if (i == variableExcluded+1):
            index = val
            if not (val in heatmap.index):
                heatmap=heatmap.append(pd.Series(name=val, dtype="float64"))
                # Set row variable name
                if label["y"] == "-1":
                    label["y"] = CSV.split("-")[i].rsplit("_",1)[0]
    
    # Gather value
    with open(os.path.join(args.folder,CSV), 'r') as f:
        death = list(csv.reader(f))[-1]
        if args.mode == 1:
            heatmap[col][index] = np.float64(death[-1].split(", ")[-2])
            
        elif args.mode == 2:
            previousDeath = np.float64(death[-1].split(", ")[-2])
            day = len(death)
            for step in reversed(death):
                nbrDeath = np.float64(step.split(", ")[-2])
                if nbrDeath < float(previousDeath):
                    heatmap[col][index] = int(day/24)
                    break
                else:
                    previousDeath = nbrDeath
                    day = day - 1

# Reorder row and col
heatmap = heatmap.sort_index().sort_index(axis=1)
if not args.quiet:
    print("Heatmap generation done")

# 3 _ Make heatmap
# 

# Saved CSV
if args.csv:
    pd.DataFrame(heatmap).to_csv(args.output + '.csv')
    if not args.quiet:
        print("CSV exported here: " + args.output + '.csv')

# Displaying dataframe as an heatmap 
plt.imshow(heatmap) 

colorLabel = ""
if args.mode == 1:
    colorLabel="Number of death"
if args.mode == 2:
    colorLabel="Day of last death"
plt.colorbar(label=colorLabel)

# Assigning labels of x/y-axis 
plt.title(args.title)
plt.xlabel(label["x"])
plt.ylabel(label["y"])
plt.xticks(range(len(heatmap)), heatmap.columns) 
plt.yticks(range(len(heatmap)), heatmap.index) 

# Fit output graph
plt.tight_layout()

# Saved PNG
plt.savefig(args.output + '.png')
if not args.quiet:
    print("PNG saved here: " + args.output + '.png')