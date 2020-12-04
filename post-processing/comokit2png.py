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
import argparse, math

import multiprocessing

import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats

# 0 _ Get/Set parameters
#
parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options]')

# Files
parser.add_argument('-i', '--inputFolder', metavar="", help='Path to folder where are saved all the COMOKIT CSV files from explorations (default: "./batch_output")', type=str, default="./batch_output")
parser.add_argument('-o', '--outputImg', metavar="", help='Where to save output graph (default: "./out" =generate=> "./out[GeneratedNumber].png")', type=str, default="./out")
parser.add_argument('-e', '--experimentName', metavar="", help='Name of the experiment (if you have several in a same folder)', type=str, default="")
parser.add_argument('-r', '--replication', metavar='', help="Number of replication per value set (default: 1)", default=1, type=int)

# PNG
parser.add_argument('-t', '--title', metavar="", help='Graph title (default: [disabled])', type=str, default="")
parser.add_argument('-V', '--variance', action='store_true', help='Process min/max with variance')
parser.add_argument('--csv', action='store_true', help='Save output as CSV file')
#parser.add_argument('-p', '--plotRow', metavar="", help='Number of line to display graphs (default: 3)', type=int, default=3)
parser.add_argument('-m', '--median', action='store_true', help='Display median curve in graph')

# Other
parser.add_argument('-q', '--quiet', action='store_true', help='Disable verbose mode')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable extra verbose')
parser.add_argument('-vv', '--extraVerbose', action='store_true', help='Enable even more extra verbose')
parser.add_argument('-c', '--cores', metavar='', help="Number of core to use (default: max number of cores)", default=multiprocessing.cpu_count(), type=int)
parser.add_argument('-s', '--stepTo', metavar='', help="Change step displayed in the graph (default: 24 -> day)", default=24, type=int)

args = parser.parse_args()

if args.extraVerbose:
    args.verbose = True

if args.verbose:
    print("\n=== Starting script ===")

# 1 _ Gathering COMOKIT datasets
#

# Get all CSV files
batch_path = args.inputFolder
onlyfiles = [f for f in listdir(batch_path) if isfile(join(batch_path, f)) and ("batchDetailed-" + args.experimentName in f)and not ("building.csv" in f)]

if args.verbose:
    print("Gathering " + str(len(onlyfiles)) + " CSV files")

# Gather all CSV data for post processing
dictionaryCSVs = {}
numberCSVs = {}
for csv_file in onlyfiles:

    replicationIndex = csv_file.rsplit('_', 1)[0].rsplit("-", 1)[1]

    df = pd.read_csv(join(batch_path, csv_file), dtype="int").reset_index(drop=True)
    if replicationIndex in dictionaryCSVs:
        # Sum new CSV with previous gathered CSVs
        dictionaryCSVs[replicationIndex] = dictionaryCSVs[replicationIndex].add(df.values)

        # Update value
        numberCSVs[replicationIndex] += 1

        if args.extraVerbose:
            print("Add extra CSV to index: " + str(replicationIndex) + " (total of " + str(numberCSVs[replicationIndex]) + " csv for this replication)")
    else:
        # Set new entry
        dictionaryCSVs[replicationIndex] = df
        numberCSVs[replicationIndex] = 1
        if args.extraVerbose:
            print("Create new replication entry - Index: " + str(replicationIndex))

if args.verbose:
    print("=== End gathering CSVs ===")

# Convert dictionnary to simplier classical 2D array
CSVs = []
for key, value in dictionaryCSVs.items():
    CSVs.append(value[:].values)

# 2.1 _ Prepare variables/functions for processing
#

output_name  = ["Susceptible", "Recovered", "Asymptomatic", "Symptomatic", "Need hospital", "Need ICU", "Death"]
output_color = ["c", "g", "b", "r", "g", "y", "m", "k"]

# Aggregation + Data processing
def processPerHour(index, graph, outputs):
    prevSum = 0
    # Set/Clear for new line
    output_CSVs = [[] for i in range(len(output_name))]

    # Collect data in files
    for i in range(len(CSVs)):
        # Create temporary 3D array
        #  [Indicator
        #    [per replication]
        #  ]
        sumStepTo = [[[] for i in range(len(CSVs))] for i in range(len(output_name))]

        # Used to handle last loop if last day end before 24h
        real_stepTo = args.stepTo

        for hour in range(args.stepTo):
            # Gather data per col/row
            if len(CSVs[i]) > (index + hour): # Check if row exist
                # Gather line data in every file
                #output_CSVs[x] = output_CSVs[x].append([int(csv[index + hour][0])])   # total_incidence
                sumStepTo[4][i].append(int(CSVs[i][index + hour][1]))   # need_hosp
                sumStepTo[5][i].append(int(CSVs[i][index + hour][2]))   # need_icu
                sumStepTo[0][i].append(int(CSVs[i][index + hour][3]))   # susceptible
                # csv[4] # latent
                sumStepTo[2][i].append(int(CSVs[i][index + hour][5]))   # asymptomatic
                sumStepTo[3][i].append(int(CSVs[i][index + hour][6]))   # presymptomatic
                sumStepTo[3][i].append(int(CSVs[i][index + hour][7]))   # symptomatic
                sumStepTo[1][i].append(int(CSVs[i][index + hour][8]))   # recovered
                sumStepTo[6][i].append(int(CSVs[i][index + hour][9]))   # dead
            else:
                # Fix value for mean when last day < 24h
                real_stepTo -= 1

        # Compile value per replication
        # Need to keep every rep for gather min/max values
        for indicator in range(len(output_name)):
            output_CSVs[indicator].append(sum(sumStepTo[indicator][i]) / real_stepTo)
    # === !Collect data in files

    # Process data
    for i in range(len(output_name)):

        if args.variance:
            meanReplication = float(sum(output_CSVs[i]) / args.replication )
            variance = float(stats.stdev(output_CSVs[i]))
            # [min, max, meanReplication]
            outputs[i][graph] = [
                max(0.0, (meanReplication - variance)),
                float(meanReplication + variance),
                meanReplication
                ]
        # Saved
        #   - Min value over replications
        #   - Max value over replications
        #   - Mean value over replications
        #   if - Median value over replications
        else:
            # [min, max, mean]
            outputs[i][graph] = [
                float(min(output_CSVs[i])),
                float(max(output_CSVs[i])),
                float(sum(output_CSVs[i]) / args.replication)
                ]

            # [min, max, mean, median]
            if args.median:
                outputs[i][graph] += [stats.median(output_CSVs[i])]

        # Verbose
        if multiprocessing.current_process().name == "Process-2" and args.extraVerbose:
            print("[Process-2 - " + str(output_name[i]) + "] : " + str(outputs[i][graph]) )
    # === !Process data

# !def processPerHour

def splitPerProcess(mini, maxi, index_graph, outputs):
    # Verbose
    if not args.quiet:
        print("[" + multiprocessing.current_process().name + "]\tStart thread processing lines ["+str(mini)+","+str(maxi)+"] with dictionnary index " + str(index_graph))

    for row in range(mini, maxi, args.stepTo):
        if row > len(CSVs[0]):
            continue

        # Process a row
        processPerHour(row, index_graph, outputs)

        if args.verbose and multiprocessing.current_process().name == "Process-2":
            iteration = ((maxi - mini) / args.stepTo)
            print("[" + multiprocessing.current_process().name + "]\tFinished gathering and processing CSVs' row " + str(row) + "\t(" + str(round(iteration - ((maxi - row) / args.stepTo), 0) + 1) + "/" + str(round(iteration, 0)+1) + " iteration)\n")
            if row == 0:
                print("\tProcessed " + str(len(CSVs) * args.stepTo) + " lines over " + str(len(output_name)) + " cols ( == " + str((len(CSVs) * args.stepTo)*len(output_name)) + " cells)\n")

        index_graph += 1


    # Verbose
    if not args.quiet:
        print("[" + multiprocessing.current_process().name + "]\tEnd thread processing lines ["+str(mini)+","+str(maxi)+"] with end index " + str(index_graph))
# !def splitPerProcess


# 2.2 _ Launch processing
#

lenCSVs = len(CSVs[0])
threads = []
manager = multiprocessing.Manager()
output = [manager.list(range( int(lenCSVs/args.stepTo) )) for i in range(len(output_name))]

if not args.quiet:
    print("Start thread processing...")
    if args.verbose:
        print("= Using " + str(args.cores) + " cores on " + str(multiprocessing.cpu_count()) + " availables")
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

if args.verbose:
    print("Quick view of some processed data :")
    print(output[0][:3])
    print("Processed " + str(len(output[0])) + " days")

# Save output CSV
if args.csv:
    pd.DataFrame(output, index=output_name).to_csv(args.outputImg + '.csv', header=None)
    if not args.quiet:
        print("CSV file saved as : " + args.outputImg + '.csv')

# 3 _ Generating image
#

if not args.quiet:
    print("Creating plot...")

col_name = ["Min", "Max", "Mean"]
if args.median:
    col_name.append("Median")

# Turn result in user-friendly DataFrame
output_df = []
for i in range(len(output)):
    output_df.append( pd.DataFrame(list(output[i]), columns=col_name) )

# Initialise the figure and axes.
numberRow=3 #args.plotRow
numberCol=3 #math.ceil(len(output_df)/numberRow)
fig, ax = plt.subplots(nrows=numberRow, ncols=numberCol, sharey='row',figsize=(10,10))

fig.suptitle( args.title )

outputIndex = 0

# Set curves
for row in range(numberRow):
    for i in range(numberCol):

        if (row != numberCol-1 and i == 2) or (outputIndex + 1 > len(output_df)):
            # Debug display
            ax[row][i].axis('off')
            continue

        ax[row][i].fill_between(output_df[outputIndex].index, output_df[outputIndex]["Min"], output_df[outputIndex]["Max"], color=output_color[outputIndex], alpha=0.2, label = "Min/Max")

        if args.median:
            ax[row][i].plot(output_df[outputIndex].index, output_df[outputIndex]["Median"], color="k", label = "Median")

        ax[row][i].plot(output_df[outputIndex].index, output_df[outputIndex]["Mean"], color=output_color[outputIndex], label = "Mean")

        ax[row][i].legend(loc="upper left", title=output_name[outputIndex], frameon=True)

        outputIndex += 1

# Set axes legends
plt.setp(ax[-1][:], xlabel='Days')
# If no loop, only set to first line...
for i in range(numberRow):
    plt.setp(ax[i][0], ylabel='Number of person')

# Save output graph
plt.tight_layout()
plt.savefig(args.outputImg + '.png', bbox_inches='tight')

if not args.quiet:
    print("Output image saved as : " + args.outputImg + '.png')
