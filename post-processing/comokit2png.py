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
outputAsymp = []
outputSymp = []
prevSum = 0
nbrSim = args.replication
index_graph = 0
simStep = 24

def processPerHour(index, graph):
    # Set/Clear for new line
    CSVs_sick = pd.DataFrame()
    CSVs_asymptomatic = pd.DataFrame()
    CSVs_symptomatic = pd.DataFrame()

    # Per file
    for csv in CSVs:
        for hour in range(simStep):            
            if len(csv[5]) > (index + hour):# and len(csv[6]) > (index + hour) and len(csv[7]) > (index + hour):
                # ['total_incidence', 'need_hosp', 'need_icu', 'susceptible', 'latent', 'asymptomatic', 'presymptomatic', 'symptomatic', 'recovered', 'dead']
                # [     0                   1           2           3             4         5               6                   7             8         9   ]
                # Gather line data in every file
                #CSVs_sick = CSVs_sick.append([int(csv[0][index])])
                CSVs_asymptomatic = CSVs_asymptomatic.append([int(csv[5][index + hour])])
                CSVs_symptomatic = CSVs_symptomatic.append([int(csv[6][index + hour])])
                CSVs_symptomatic = CSVs_symptomatic.append([int(csv[7][index + hour])])
            #else:
            #    print("[Exception] len(csv[5]) " + str(len(csv[5])) + " > ("+str(index)+" + "+str(hour)+")")
            #    print("[Exception] len(csv[6]) " + str(len(csv[6])) + " > ("+str(index)+" + "+str(hour)+")")
            #    print("[Exception] len(csv[7]) " + str(len(csv[7])) + " > ("+str(index)+" + "+str(hour)+")")

    ## Process and write data
    #outputSick.append([
    #    float(CSVs_sick.min()),
    #    float(CSVs_sick.max()), 
    #    float(CSVs_sick.mean()),
    #    float(CSVs_sick.std()),
    #    -1,
    #    # Incidence
    #    float(CSVs_sick.sum() / nbrSim),
    #    float((CSVs_sick.sum() - prevSum) / nbrSim)
    #])
    #
    ## Save actual sum for next loop
    #prevSum = CSVs_sick.sum()
    #
    ## Compute variance only if needed
    ## -> Save performances
    #if args.variance:
    #    outputSick[-1][4] = float(CSVs_sick.var())
    
    # Process asymptomatic
    # [min, max, mean]
    asymptoVariance = float(CSVs_asymptomatic.std())
    asymptoMean = float(CSVs_asymptomatic.mean())
    outputAsymp.insert(graph, [
        max(0.0, (asymptoMean - asymptoVariance)),
        (asymptoMean + asymptoVariance),
        asymptoMean
        ])

    # Process symptomatic
    # [min, max, mean]
    symptoVariance = float(CSVs_symptomatic.std())
    symptoMean = float(CSVs_symptomatic.mean())
    outputSymp.insert(graph, [
        max(0.0, (symptoMean - symptoVariance)),
        (symptoMean + symptoVariance),
        symptoMean
        ])

    # command process follow
    #if (index % 500) == 0 and not args.quiet:
    #    print(outputAsymp[graph])
    #    print(str(index)+" / "+str(len(CSVs[0])))
    # !def processPerHour

def splitPerProcess(mini, maxi, index_graph):
    for row in range(mini, maxi, simStep):
        if row > len(CSVs[0]):
            continue

        processPerHour(row, index_graph)

        index_graph += 1
    # !def splitPerProcess

# Per row
import multiprocessing

threads = []
print("Start thread processing...")
#for row in range(0,len(CSVs[0]),simStep):  # ~ 49m 50s 
#
#    if row > len(CSVs[0]):
#        continue
#
#    processPerHour(row, index_graph)
#    #x = threading.Thread(target=processPerHour, args=(row, index_graph,))
#    ##x = multiprocessing.Process(target=processPerHour, args=(row, index_graph,))
#    #threads.append(x)
#    #x.start()
#
#    index_graph += 1

cores = 8
# Create a thread per core
for split in range(cores):

    step = int(len(CSVs[0]) / cores)
    mini = int(step * split)

    x = multiprocessing.Process(target=splitPerProcess, args=(mini, (mini + step -1), int(mini / simStep) ) )
    threads.append(x)
    x.start()

# Wait all thread to terminate
for index, thread in enumerate(threads):
    thread.join()

print("Creating plot...")
# Turn result in user-friendly DataFrame
col_name = ["Min", "Max", "Mean"]#, "Standard deviation", "Variance", "Incidence cumul", "Incidence"]
#df_tmp = pd.DataFrame(outputSick, columns=col_name)
time = pd.date_range('1/1/2000', periods=len(CSVs), freq='1h')
df_tmp = pd.DataFrame(outputAsymp, columns=col_name)
df_tmp1 = pd.DataFrame(outputSymp, columns=col_name)


# 2 _ Generating image
# 

# Initialise the figure and axes.
fig, ax = plt.subplots(1, 2, sharey=True)

fig.suptitle( args.title )

# Set curves
ax[0].fill_between(df_tmp1.index, df_tmp["Min"], df_tmp["Max"], color='b', alpha=0.2, label = "Min/Max")
ax[0].plot(df_tmp1.index, df_tmp["Mean"], label = "Mean")#(df_tmp1.index, df_tmp["Mean"], label = "Mean")
ax[0].legend(loc="upper left", title="Asymp", frameon=True)

ax[1].fill_between(df_tmp1.index, df_tmp1["Min"], df_tmp1["Max"], color='r', alpha=0.2, label = "Min/Max")
ax[1].plot(df_tmp1.index, df_tmp1["Mean"], label = "Mean", color='r')
ax[1].legend(loc="upper left", title="Symp", frameon=True)
#for name in col_name[2:4]:
#    ax.plot(df_tmp.index, df_tmp[name], label = name)
#
#if args.variance:
#    ax.plot(df_tmp.index, df_tmp["Variance"], label = "variance")
#
#ax.bar(df_tmp.index, df_tmp["Incidence"], color="r", label = "Incidence")

# Place legend
#plt.legend(loc="upper left", title="Legend", frameon=True)

# Save output graph
imgName = args.outputImg + str(len([f for f in listdir("./") if isfile(join("./", f)) and ("out" in f)])) + '.png'
plt.savefig(imgName, bbox_inches='tight')

if not args.quiet:
    print("Output image saved as : "+imgName)