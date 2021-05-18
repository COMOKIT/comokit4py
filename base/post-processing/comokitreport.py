import os
import os.path as path
import pandas as pd
import numpy as np
import functools as fp

fp.map = lambda f, x: list(map(f, x))

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

	returns = list(replicationData.values())
	for repData in returns:
		repData.columns = __columns
	return returns

def deviationDf(df):
	return df.mean()

def renameDf(df, columns):
	df.columns = columns
	return df

def proportion(df):
	df.columns
	return proportion

def scaleDF(df):
	"""
	Scale dataframe `df` to 100k agents
	"""
	totalAgents = sum(df.loc[1, :][1:-1])
	return (df / totalAgents * 100000).round().astype(int)

def firstDay(df):
	df = scaleDF(df)
	firstNZ = lambda columnName: df[df[columnName] > 0].first_valid_index()
	df = pd.DataFrame(map(firstNZ, __columns))
	df.columns = ["First day of:"]
	df = df.transpose()
	df.columns = __columns
	return df

def generateReport(gatheredData):
	# scale to 100k
	gatherData = map(scaleDF, gatheredData)

	def byColumn(f, column, df):
		# f: min or max
		index = f(df[[column]])
		return df.loc[index, :]
	minByColumn = fp.partial(byColumn, lambda df: df.idxmin())
	maxByColumn = fp.partial(byColumn, lambda df: df.idxmax())

	minDf = lambda df: df.min()
	maxDf = lambda df: df.max()
	avgDf = lambda df: df.avg()
	# aggregations
	meanAgg = pd.DataFrame(map(lambda df: df.mean(), gatheredData))
	minAgg = pd.DataFrame(map(lambda df: df.min(), gatheredData))
	maxAgg = pd.DataFrame(map(lambda df: df.max(), gatheredData))
	# declare list of statistics
	meanCases = meanAgg.mean().round().astype(int)
	minCases = minAgg.min().round().astype(int)
	maxCases = maxAgg.max().round().astype(int)
	def calculateProportion(d):
		mean = d.mean()
		return mean / mean.total
	#proportion = pd.DataFrame(map(calculateProportion, meanAgg), meanAgg)
	stats = {"mean": meanCases, "proportion": np.round(meanCases / meanCases.total * 100).astype(int)}
	def aux(col):
		stats["min " + col] = minByColumn(col, minAgg).min().round().astype(int)
		stats["max " + col] = maxByColumn(col, maxAgg).max().round().astype(int)
	list(map(aux, [
		"hospitalisation",
		"ICU",
		"susceptible",
		"recovered",
		"dead"]))
	result = pd.DataFrame(stats.values())
	# rename the rows
	result = result.transpose()
	result.columns = list(stats.keys())
	return result.transpose()
