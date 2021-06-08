import os
import os.path as path
import pandas as pd
import numpy as np
import functools as fp

fp.map = lambda f, x: list(map(f, x))

# list of columns ordered by appearing order in csv
__columns = [
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

@fp.singledispatch
def scaleDF(*args, **kwargs):
	raise(Exception("Method not defined"))

@scaleDF.register(pd.DataFrame)
def _(df):
	"""
	Scale dataframe `df` to 100k agents
	"""
	totalAgents = max(df[['total incident']])
	return (df / totalAgents * 100000).round().astype(int)

@scaleDF.register(list)
def _(dfs):
	assert(type(dfs[0]) != pd.DataFrame, "scaleDF input list must be of type DataFrame")
	return list(map(scaleDF, dfs))

def generateReport(gatheredData, scaled = True):
	# scale to 100k
	data = scaleDF(gatheredData) if scaled else gatheredData

	# sample size
	n = len(gatheredData)

	# list of aggregations
	aggregations = {
			"Min": lambda df: df.min(),
			"Max": lambda df: df.max(),
			"First day": lambda df: pd.Series(map(
				lambda c: df[df[c] > 0].first_valid_index() / 24
				, __columns)).transpose(),
			"Last day": lambda df: pd.Series(map(
				lambda c: df[df[c] > 0].last_valid_index() / 24
				, __columns)).transpose()
			}

	# perform aggregate, return dataframe of mean and std
	def aggregate(k):
		f = aggregations[k]
		#sumData = f(gatheredData[0]).fillna(0)
		#count = 1
		## mean
		#for df in gatheredData[1:-1]:
		#	stat = f(df)
		#	for c in __columns:
		#		if stat[c] == np.nan:
		#			stat[c] = sumData[c] / n
		#	sumData = sumData + stat
		#	count = count + 1

		#mean = sumData / count
		aggData = list(map(f, gatheredData))
		mean = sum(aggData) / n
		# std
		# Python iterators are stateful -_-
		std = map(lambda df: (df - mean).pow(2), aggData)
		std = (sum(std) / n).pow(0.5)
		std = pd.DataFrame(std)
		std.columns = ["Std. " + k]
		std = std.transpose()
		std.columns = __columns

		mean = pd.DataFrame(mean)
		mean.columns = [k]
		mean = mean.transpose()
		mean.columns = __columns
		return pd.concat([mean, std])

	series = [pd.DataFrame(aggregate(k)) for k in aggregations]
	result = pd.concat(series).round().astype(int)
	result.drop('total incident', axis=1, inplace=True)
	return result
