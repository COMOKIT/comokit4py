import comokit4py
import os
from testfacility import test, testheader

# TODO: make this test less dependent on environment

testheader("GAMA Test")

gamaPath = os.getenv("GAMA_HOME")
if gamaPath is None:
	gamaPath = "../../../../.local/share/GAMA_1.8.1_Linux"

gamaPathHeadless = os.path.join(gamaPath,"headless/gama-headless.sh")

def name(name_):
	return "GAMA Test: %s" % name_

gama = comokit4py.Gama(gamaPathHeadless)

# Abbreviate:
# - r = retrieved

@test("Script path")
def _():
	scriptPath = os.path.abspath(gamaPathHeadless)
	rScriptPath = gama.getPathToHeadlessScript()
	return scriptPath == rScriptPath

@test("Base directory")
def _():
	basedir = os.path.abspath(gamaPath)
	rBasedir = gama.getBaseDir()
	return basedir == rBasedir

@test("Version string")
def _():
	return gama.getVersion() == "1.8.1"

@test("Memory string")
def _():
	result = gama.getMemory() == "4096m"
	gama.setMemory("4g")
	return result and gama.getMemory() == "4g"
