from importlib import import_module
from functools import partial

def writelog(prefix, *msg):
	print("[%s]" % prefix, *msg)

info = partial(writelog, "INFO")
error = partial(writelog, "ERROR")
success = partial(info, "Success: ")
failed = partial(info, "Failed: ")

def testset(name, modulename):
	testmodule = import_module(modulename)
	try:
		result = testmodule.runtests()
		if result:
			success(name)
		else:
			failed(name)
	except Exception as e:
		error("Test %s errored: %s" % (name, e))
		raise e

testset("XML Generation Test", "regression")
