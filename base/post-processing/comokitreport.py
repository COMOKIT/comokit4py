import os
import os.path as path
import pandas as pd
import numpy as pd
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
		"recovered",
		"dead"
		]

# An invert indices for easier lookup
__invColumns = dict(map(lambda pair: (pair[1], pair[0]), enumerate(__columns)))

def mapreduce(fmap, freduce, itr, initial = None):
	"""
	mapreduce(fmap, freduce, itr[, initial])
	---
	Perform `map(fmap, itr)`, then perform `functools.reduce(freduce, result)` and return the final result. Initial is passed to reduce

	mapreduce(lambda x: x + 1, lambda x, y: x * y, [0,1,2]) == 6
	"""
	mapped = map(fmap, itr)
	if initial is None:
		return fp.reduce(freduce, mapped)
	else:
		return fp.reduce(freduce, mapped, initial = initial)

def __columnGetter(field):
	"""
	__columnGetter(field)
	---
	Return a function that get the corresponding column in the output data. `field` must be one of `__columns`.
	"""
	assert(field in __columns)
	index = __invColumns[field]
	def aux(data):
		return data[:, index]
	
getTotal = __columnGetter("total")
getHospitalisation = __columnGetter("hospitalisation")
getICU = __columnGetter("ICU")
getSusceptible = __columnGetter("susceptible")
getLatent = __columnGetter("latent")
getAsymptomatic = __columnGetter("asymptomatic")
getPresymtomatic = __columnGetter("presymtomatic")
getRecovered = __columnGetter("recovered")
getDead = __columnGetter("dead")
