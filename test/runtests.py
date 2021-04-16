from testfacility import runtests
from os import _exit as exit
from importlib import import_module
# Import tests
import regression
import testGama
import testGamaExperiment

result = runtests()
if result:
	exit(0)
else:
	exit(-1)
