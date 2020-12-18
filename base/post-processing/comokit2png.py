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
parser.add_argument('-S', '--displayStep', metavar='', help="Change x index scale in png (default: 24 -> day)", default=24, type=int)
parser.add_argument('-m', '--median', action='store_true', help='Display median curve in graph')
parser.add_argument('-Q', '--quartile', action='store_true', help='Display quartile curves in graph (override median option)')

parser.add_argument('-d', '--startDate', metavar=("YYYY", "MM", "DD"), nargs = 3, help = 'Set starting real date in PNG x axis')
parser.add_argument('-p', '--startPolicy', metavar=("YYYY", "MM", "DD"), nargs = 3, help = 'Set starting policy grey area in PNG (needs --startDate and --endPolicy)')
parser.add_argument('-P', '--endPolicy', metavar=("YYYY", "MM", "DD"), nargs = 3, help = 'Set starting policy grey area in PNG (needs --startDate and --startPolicy)')

# Other
parser.add_argument('-q', '--quiet', action='store_true', help='Disable verbose mode')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable extra verbose')
parser.add_argument('-vv', '--extraVerbose', action='store_true', help='Enable even more extra verbose')
parser.add_argument('-c', '--cores', metavar='', help="Number of core to use (default: max number of cores)", default=multiprocessing.cpu_count(), type=int)
parser.add_argument('-s', '--stepTo', metavar='', help="Compile several steps in one (default: 1 -> disable)", default=1, type=int)

# Magic
parser.add_argument('--azure', action='store_true', help='Tweak display for COMOKIT-Azure purpose')

args = parser.parse_args()

# Apply predefined tweaks
# without overriding potentially already set
if args.azure:
    if not args.quiet:
        print("=== Apply missing parameter for Azure project ===")
    if not args.startDate:
        args.startDate = [2020, 1, 24]
        if not args.quiet:
            print("\tSet --startDate", args.startDate)
    if not args.startPolicy:
        args.startPolicy = [2020, 3, 17]
        if not args.quiet:
            print("\tSet --startPolicy", args.startPolicy)
    if not args.endPolicy:
        args.endPolicy = [2020, 5, 11]
        if not args.quiet:
            print("\tSet --endPolicy", args.endPolicy)
    if args.replication == 1: # Default value
        args.replication = 50
        if not args.quiet:
            print("\tSet --replication", args.replication)
    if not args.quiet:
        print("=== Done ===\n")

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
        if len(dictionaryCSVs[replicationIndex]) < len(df):
            dictionaryCSVs[replicationIndex] = dictionaryCSVs[replicationIndex].add(df, fill_value = 0)
        elif len(dictionaryCSVs[replicationIndex]) > len(df):
            dictionaryCSVs[replicationIndex] = df.add(dictionaryCSVs[replicationIndex], fill_value = 0)
        else:
            dictionaryCSVs[replicationIndex] = dictionaryCSVs[replicationIndex].add(df)

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

output_name  = ["Susceptible", "Recovered", "Presymptomatic", "Asymptomatic", "Symptomatic", "Need hospital", "Need ICU", "Death"]
output_color = ["g", "b", "olive", "lightgreen", "y", "orange", "r", "m"]

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
                sumStepTo[5][i].append(int(CSVs[i][index + hour][1]))   # need_hosp
                sumStepTo[6][i].append(int(CSVs[i][index + hour][2]))   # need_icu
                sumStepTo[0][i].append(int(CSVs[i][index + hour][3]))   # susceptible
                # csv[4] # latent
                sumStepTo[3][i].append(int(CSVs[i][index + hour][5]))   # asymptomatic
                sumStepTo[2][i].append(int(CSVs[i][index + hour][6]))   # presymptomatic
                sumStepTo[4][i].append(int(CSVs[i][index + hour][7]))   # symptomatic
                sumStepTo[1][i].append(int(CSVs[i][index + hour][8]))   # recovered
                sumStepTo[7][i].append(int(CSVs[i][index + hour][9]))   # dead
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
        #   if - Quartile [Q1, Q2, Q3] value over replications
        #   if - Median value over replications
        else:
            # [min, max, mean]
            outputs[i][graph] = [
                float(min(output_CSVs[i])),
                float(max(output_CSVs[i])),
                float(sum(output_CSVs[i]) / args.replication)
                ]

            if args.quartile:
                import numpy as np
                # [min, max, mean, q1, q2, q3]
                outputs[i][graph] += [np.quantile(output_CSVs[i], .25), 
                np.quantile(output_CSVs[i], .50),
                np.quantile(output_CSVs[i], .75)]
            else:
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
            if row == 0 or args.extraVerbose:
                print("[" + multiprocessing.current_process().name + "]\tFinished gathering and processing CSVs' row " + str(row) + "\t(" + str(round(iteration - ((maxi - row) / args.stepTo), 0) + 1) + "/" + str(round(iteration, 0)+1) + " iteration)")
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
for csv in CSVs:
    lenCSVs = min(lenCSVs, len(csv))

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
    x = multiprocessing.Process(target=splitPerProcess, args=(mini, min(lenCSVs, mini + step + min(5, args.cores)), int(mini / args.stepTo), output ) )
    threads.append(x)
    x.start()

# Wait all thread to terminate
for index, thread in enumerate(threads):
    thread.join()

# Clean oversized array
for i in range(len(output)):
    out = output[i]
    output[i] = [item for item in out if not isinstance(item, int)]

if args.verbose:
    print("Array form : ", len(output), "x", len(output[0]), "x", len(output[0][0]))
    if args.extraVerbose:
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

if args.quartile:
    col_name.append("Q1 quartile")
    col_name.append("Q2 quartile")
    col_name.append("Q3 quartile")
else:
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

# Fake x axis aggregation
index = [x / args.displayStep for x in range(len(output_df[0]))]
policyTime = None

# Change x axis display with dates
if (args.startDate 
    and len(args.startDate) == 3):
    # Add needed library
    import datetime 
    from matplotlib.dates import DateFormatter, drange
    import matplotlib.transforms as mtransforms

    # Change un-named days to real date
    date1 = datetime.datetime(int(args.startDate[0]), int(args.startDate[1]), int(args.startDate[2])) 
    index = drange(date1, 
        date1 + datetime.timedelta( hours = len(output_df[0]) ), 
        datetime.timedelta(hours = args.stepTo) 
        )

    # Format display date
    formatter = DateFormatter('%m-%d')
    for axis in ax:
        for a in axis:
            a.xaxis.set_major_formatter(formatter)
            fig.autofmt_xdate(rotation=25)

    # Prepare policy time area
    if ((args.startPolicy and args.endPolicy) # Check if parameters are set
        and ((len(args.startPolicy) == 3) and (len(args.endPolicy) == 3))): # Check if properly set

        policyTimeDate = [ drange(datetime.datetime(int(args.startPolicy[0]), int(args.startPolicy[1]), int(args.startPolicy[2])), datetime.datetime(int(args.endPolicy[0]), int(args.endPolicy[1]), int(args.endPolicy[2])), datetime.timedelta(hours = args.stepTo))[i] for i in (0, -1) ]
        policyTime = []
        for i in index:
            if policyTimeDate[0] < i and i  < policyTimeDate[-1]:
                policyTime.append(True)
            else:
                policyTime.append(False)

outputIndex = 0

# Set curves
for row in range(numberRow):
    for i in range(numberCol):

        if (row == 0 and i == 2) :
            # Debug display
            ax[row][i].axis('off')
            continue

        if policyTime is not None:
            # Draw policy area
            ax[row][i].fill_between(index, 0, 1, where=policyTime, 
                            facecolor='grey', alpha=0.25, transform=mtransforms.blended_transform_factory(ax[row][i].transData, ax[row][i].transAxes))

        ax[row][i].fill_between(index, output_df[outputIndex]["Min"], output_df[outputIndex]["Max"], color=output_color[outputIndex], alpha=0.2, label = "Min/Max")
        if args.quartile:
            ax[row][i].plot(index, output_df[outputIndex]["Q1 quartile"], color="k", linestyle='dotted', label = "Q1 quartile")
            ax[row][i].plot(index, output_df[outputIndex]["Q2 quartile"], color="k", linestyle='solid', label = "Q2 quartile")
            ax[row][i].plot(index, output_df[outputIndex]["Q3 quartile"], color="k", linestyle='dashed', label = "Q3 quartile")
        else:
            if args.median:
                ax[row][i].plot(index, output_df[outputIndex]["Median"], color="k", label = "Median")

        ax[row][i].plot(index, output_df[outputIndex]["Mean"], color=output_color[outputIndex], label = "Mean")

        ax[row][i].legend(loc="upper left", title=output_name[outputIndex], frameon=True)

        if args.verbose:
            print("Finished " + str(output_name[outputIndex]))

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
