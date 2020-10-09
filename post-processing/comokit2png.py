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

import multiprocessing

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
#parser.add_argument('-p', '--plotRow', metavar="", help='Number of line to display graphs (default: 1)', type=int, default=1)

# Other
parser.add_argument('-q', '--quiet', action='store_true', help='Disable verbose mode')
parser.add_argument('-c', '--cores', metavar='', help="Number of core to use (default: max number of cores)", default=multiprocessing.cpu_count(), type=int)
parser.add_argument('-s', '--stepTo', metavar='', help="Change step displayed in the graph (default: 24 -> day)", default=24, type=int)

args = parser.parse_args()

# 1 _ Gathering COMOKIT datasets
# 

# Get all CSV files
batch_path = args.inputFolder
onlyfiles = [f for f in listdir(batch_path) if isfile(join(batch_path, f)) and ("batchDetailed-" in f)and not ("building.csv" in f)]

# Gather all CSV data for post processing
CSVs = []
for csv_file in onlyfiles:        
    df = pd.read_csv(join(batch_path, csv_file), header=None).iloc[1:].reset_index(drop=True)
    CSVs.append(df)


# 2.1 _ Prepare variables/functions for processing
# 

output_name  = ["Asymptomatic", "Symptomatic", "Need hospital", "Need ICU", "Death", "Susceptible", "Recovered"]
output_color = ["b", "r", "g", "y", "m", "k", "c", "g"]

# Aggregation + Data processing
def processPerHour(index, graph, outputs):
    prevSum = 0
    # Set/Clear for new line
    CSVs_sick = pd.DataFrame()
    output_CSVs = [pd.DataFrame() for i in range(len(output_name))]

    # Per file
    for csv in CSVs:
        for hour in range(args.stepTo):
            # Gather data per col/row
            if len(csv[5]) > (index + hour): # Check if row exist
                # Gather line data in every file
                #CSVs_sick = CSVs_sick.append([int(csv[0][index])])                   # total_incidence
                output_CSVs[2] = output_CSVs[2].append([int(csv[1][index + hour])])   # need_hosp
                output_CSVs[3] = output_CSVs[3].append([int(csv[2][index + hour])])   # need_icu
                output_CSVs[5] = output_CSVs[5].append([int(csv[3][index + hour])])   # susceptible
                # latent
                output_CSVs[0] = output_CSVs[0].append([int(csv[5][index + hour])])   # asymptomatic
                output_CSVs[1] = output_CSVs[1].append([int(csv[6][index + hour])])   # presymptomatic
                output_CSVs[1] = output_CSVs[1].append([int(csv[7][index + hour])])   # symptomatic
                output_CSVs[6] = output_CSVs[6].append([int(csv[8][index + hour])])   # recovered
                output_CSVs[4] = output_CSVs[4].append([int(csv[9][index + hour])])   # dead
    
    # Process data
    for i in range(len(output_name)):
        variance = float(output_CSVs[i].std())
        mean = float(output_CSVs[i].mean())
        
        # [min, max, mean]
        outputs[i][graph] = [
            max(0.0, (mean - variance)),
            (mean + variance),
            mean
            ]
# !def processPerHour

def splitPerProcess(mini, maxi, index_graph, outputs):
    for row in range(mini, maxi, args.stepTo):
        if row > len(CSVs[0]):
            continue

        # Process a row
        processPerHour(row, index_graph, outputs)

        index_graph += 1

    # Verbose
    if not args.quiet:
        print("End thread processing lines ["+str(mini)+","+str(maxi)+"] with end index " + str(index_graph))
# !def splitPerProcess


# 2.2 _ Launch processing
# 

lenCSVs = len(CSVs[0])
threads = []
manager = multiprocessing.Manager()
output = [manager.list(range( int(lenCSVs/args.stepTo) )) for i in range(len(output_name))]

if not args.quiet:
    print("Start thread processing...")
# Create a thread per core
for split in range(args.cores):

    step = int(lenCSVs / args.cores)
    mini = int(step * split)

    # Start a thread on a core
    x = multiprocessing.Process(target=splitPerProcess, args=(mini, (mini + step -1), int(mini / args.stepTo), output ) )
    threads.append(x)
    x.start()

# Wait all thread to terminate
for index, thread in enumerate(threads):
    thread.join()

if not args.quiet:
    print("Quick view of some processed data :")
    print(output[0][:3])
    print("Processed " + str(len(output)) + " days")

# 3 _ Generating image
# 

if not args.quiet:
    print("Creating plot...")

col_name = ["Min", "Max", "Mean"]

# Turn result in user-friendly DataFrame
output_df = []
for i in range(len(output)):
    output_df.append( pd.DataFrame(list(output[i]), columns=col_name) )

# Initialise the figure and axes.
fig, ax = plt.subplots(1, len(output_df), figsize=(10,3), sharey=True)

fig.suptitle( args.title )

# Set curves
for i in range(len(output_df)):
    ax[i].fill_between(output_df[i].index, output_df[i]["Min"], output_df[i]["Max"], color=output_color[i], alpha=0.2, label = "Min/Max")
    ax[i].plot(output_df[i].index, output_df[i]["Mean"], color=output_color[i], label = "Mean")
    ax[i].legend(loc="upper left", title=output_name[i], frameon=True)

# Set axes legends
plt.setp(ax[:], xlabel='Days')
plt.setp(ax[0], ylabel='Number of person')

# Save output graph
imgName = args.outputImg + str(len([f for f in listdir("./") if isfile(join("./", f)) and ("out" in f)])) + '.png'
plt.savefig(imgName, bbox_inches='tight')

if not args.quiet:
    print("Output image saved as : "+imgName)