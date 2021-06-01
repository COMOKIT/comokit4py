import os
import os.path as path
import pandas as pd
import numpy as np
import functools as fp
from . import common

fp.map = lambda f, x: list(map(f, x))

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
	totalAgents = max(df[common.COLUMNS[0]])
	return (df.values / totalAgents * 100000).round().astype(int)

@scaleDF.register(list)
def _(dfs):
	assert(type(dfs[0]) != (pd.DataFrame), "scaleDF input list must be of type DataFrame")
	return [scaleDF(df) for df in dfs]

@fp.singledispatch
def generateReport(*args, **kwargs):
	raise(common.NotImplemented)

@generateReport.register(list)
def _(gatheredData, scaled = True):
	assert(type(gatheredData[0]) != (pd.DataFrame), "scaleDF input list must be of type DataFrame")

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
				, common.COLUMNS)).transpose(),
			"Last day": lambda df: pd.Series(map(
				lambda c: df[df[c] > 0].last_valid_index() / 24
				, common.COLUMNS)).transpose()
			}

	# perform aggregate, return dataframe of mean and std
	def aggregate(k):
		f = aggregations[k]
		aggData = list(map(f, gatheredData))
		mean = sum(aggData) / n
		# std
		# Python iterators are stateful -_-
		std = map(lambda df: (df - mean).pow(2), aggData)
		std = (sum(std) / n).pow(0.5)
		std = pd.DataFrame(std)
		std.columns = ["Std. " + k]
		std = std.transpose()
		std.columns = common.COLUMNS

		mean = pd.DataFrame(mean)
		mean.columns = [k]
		mean = mean.transpose()
		mean.columns = common.COLUMNS
		return pd.concat([mean, std])

	series = [pd.DataFrame(aggregate(k)) for k in aggregations]
	result = pd.concat(series).round().astype(int)
	result.drop('total incident', axis=1, inplace=True)
	return result

@generateReport.register(str)
def _(batchDir, experimentName, scaled = True):
	data = common.gatheredData(batchDir, experimentName)
	generateReport(data, scaled)
