import os
import os.path as path
import pandas as pd
import numpy as np
import functools as fp

COLUMNS = [
		"total incident",
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
INV_COLUMNS = dict(map(lambda pair: (pair[1], pair[0]), enumerate(COLUMNS)))



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
	returns = list(replicationData.values())
	for repData in returns:
		repData.columns = COLUMNS
	return returns
