#!/usr/bin/python3

##################################################
## Python script to generate PNG graphs from COMOKIT exploration
## To use it you should write it like so :
#
## $ python3 comokit2png.py [-h]
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMOKIT-HPC
## Licence: LGPL 3.0
## Version: 1.0.0
## Maintainer: RoiArthurB
##################################################

from os import listdir
from os.path import isfile, join
import argparse

import pandas as pd
import matplotlib.pyplot as plt

# 0 _ Get/Set parameters
# 
parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options]')

# Files
parser.add_argument('-i', '--inputFolder', metavar="", help='Path to folder where are saved all the COMOKIT CSV files from explorations (default: "./batch_output")', type=str, default="./batch_output")
parser.add_argument('-o', '--outputImg', metavar="", help='Where to save output graph (default: "./out" =generate=> "./out[GeneratedNumber].png")', type=str, default="./out")
parser.add_argument('-r', '--replication', metavar='', help="Number of replication per value set (default: 1)", default=1, type=int)

# PNG
parser.add_argument('-t', '--title', metavar="", help='Graph title (default: "Sickness")', type=str, default="Sickness")
parser.add_argument('-v', '--variance', action='store_true', help='Enable variance curve (may crap the output index)')

# Other
parser.add_argument('-q', '--quiet', action='store_true', help='Disable verbose mode')

args = parser.parse_args()


# 1 _ Processing
# 

# Get all CSV files
batch_path = args.inputFolder
onlyfiles = [f for f in listdir(batch_path) if isfile(join(batch_path, f)) and not ("building.csv" in f)]

# Gather all CSV data for post processing
CSVs = []
for csv_file in onlyfiles:        
    df = pd.read_csv(join(batch_path, csv_file), header=None).iloc[1:].reset_index(drop=True)
    CSVs.append(df)

# Aggregation + Data processing
outputSick = []
prevSum = 0
nbrSim = args.replication

# Per row
for row in range(len(CSVs[0])):
    # Set/Clear for new line
    CSVs_sick = pd.DataFrame()
    
    # Per file
    for csv_index in range(len(CSVs)):
        # Gather line data in every file
        CSVs_sick = CSVs_sick.append([int(CSVs[csv_index][0][row])])

    # Process and write data
    outputSick.append([
        float(CSVs_sick.min()),
        float(CSVs_sick.max()), 
        float(CSVs_sick.mean()),
        float(CSVs_sick.std()),
        float(CSVs_sick.var()),
        # Incidence
        float(CSVs_sick.sum() / nbrSim),
        float((CSVs_sick.sum() - prevSum) / nbrSim)
    ])
    
    prevSum = CSVs_sick.sum()
        
    if (row % 500) == 0 and not args.quiet:
        print(outputSick[-1])
        print(str(row)+" / "+str(len(CSVs[0])))

# Turn result in user-friendly DataFrame
col_name = ["Min", "Max", "Mean", "Standard deviation", "Variance", "Incidence cumul", "Incidence"]
df_tmp = pd.DataFrame(outputSick, columns=col_name)


# 2 _ Generating image
# 

# Initialise the figure and axes.
fig, ax = plt.subplots()

fig.suptitle( args.title )

# Set curves
ax.fill_between(df_tmp.index, df_tmp["Min"], df_tmp["Max"], color='b', alpha=0.2, label = "Min/Max")
for name in col_name[2:3]:
    ax.plot(df_tmp.index, df_tmp[name], label = name)

if args.variance:
    ax.plot(df_tmp.index, df_tmp["Variance"], label = "variance")

ax.bar(df_tmp.index, df_tmp["Incidence"], label = "Incidence")

# Place legend
plt.legend(loc="upper left", title="Legend", frameon=True)

# Save output graph
imgName = args.outputImg + str(len([f for f in listdir("./") if isfile(join("./", f)) and ("out" in f)])) + '.png'
plt.savefig(imgName, bbox_inches='tight')

if not args.quiet:
    print("Output image saved as : "+imgName)