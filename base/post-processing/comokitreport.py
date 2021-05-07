import os
import os.path as path
import pandas as pd
import numpy as np
from comomkit4py.comokit2png import gatheringCSV

# list of columns ordered by appearing order in csv
__columns = [
		"total",
		"hospitalisation",
		"ICU",
		"susceptible",
		"latent",
		"asymptomatic",
		"presymtomatic",
		"symtomatic",
		"recovered",
		"dead"
		]

# An invert indices for easier lookup
__invColumns = dict(map(lambda pair: (pair[1], pair[0]), enumerate(__columns)))

def mapreduce(fmap, freduce, itr):
	"""
	mapreduce(fmap, freduce, itr)
	---
	Perform `map(fmap, itr)`, then perform `functools.reduce(freduce, result)` and return the final result.

	mapreduce(lambda x: x + 1, lambda x, y: x * y, [0,1,2]) == 6
	"""
	mapped = map(fmap, itr)
	return fp.reduce(freduce, mapped)

def gatherData(batchDir: str, experimentName: str) -> list:
	# all the csv file that fit the format we wanted
	dataFiles = [f for f in os.listdir(batchDir) if
			path.isfile(path.join(batchDir, f))
			and ("batchDetailed-" + experimentName in f)
			and not ("building.csv" in f)]
	# dictionary holds the total population data of each replication
	# key = replication
	replicationData = {}
	for dataFile in dataFiles:
		replicationIndex = dataFile.rsplit('_', 1)[0].rsplit("-", 1)[1]
		data = pd.read_csv(path.join(batchDir, dataFile), dtype="int").reset_index(drop = True)
		if replicationIndex not in replicationData:
			replicationData[replicationIndex] = data
		else:
			replicationData[replicationIndex] += data
	return list(replicationData.values())
