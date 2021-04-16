from importlib import import_module
import functools as f
from functools import partial, reduce

def writelog(prefix, *msg):
	print("[%s]" % prefix, *msg)

info = f.partial(writelog, "INFO")
error = f.partial(writelog, "ERROR")
success = f.partial(info, "Success: ")
failed = f.partial(info, "Failed: ")

__allTests = []

def test(name):
	def wrapper(testfunc):
		def runtest():
			try:
				result = testfunc()
				if result:
					success(name)
				else:
					failed(name)
				return result
			except Exception as e:
				error("Test %s errored: %s" % (name, e))
				return False
		__allTests.append(runtest)
		return runtest
	return wrapper

def runtests():
	call = lambda x: x()
	land = lambda x, y: x and y
	result = map(call, __allTests)
	result = list(result)
	result.append(True)
	result = f.reduce(land, list(result))
	return result
