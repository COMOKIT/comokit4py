import comokit4py
import os
from testfacility import test, testheader, testdir

# TODO: Maybe get the info inside the XML instead of just getting fields?

testheader("Gama Experiment")

basedir = testdir()
gamlFile = os.path.join(basedir, "TestExperiment.gaml")
explo = comokit4py.GamaExploration(
		experimentName = "HeadlessComparison",
		gamlFile = gamlFile,
		replication = 1,
		final = 5000,
		experimentPerXML  = 8)
explo.calculatesExperimentSpace()

@test("Experiment name")
def _():
	return explo.getExperimentName() == "HeadlessComparison"

@test("Experiment name")
def _():
	return explo.getGamlFile() == os.path.abspath(gamlFile)

@test("XML output's name")
def _():
	return explo.getXmlOutputName() == "headless.xml"

@test("Replication")
def _():
	return explo.getReplication() == 1

@test("Experiment per XML")
def _():
	return explo.getExperimentPerXML() == 8

@test("End condition")
def _():
	return explo.getUntil() == ""

@test("Simulation seed")
def _():
	return explo.getSeed() == 0

@test("List of parameters")
def _():
	return len(explo.getParametersList()) == 3

@test("Parameter combination")
def _():
	# See TestExperiment.gaml
	# The variable are scaled up because python doesn't support float range
	# Basic viral release
	p1 = range(1, 11, 1)
	# Basic viral decrease
	p2 = range(2, 21, 2)
	# End of range should not be included...
	result = 11 not in p1
	spaceSize = len(p1) * len(p2)
	return result and len(explo.getExperimentSpace()) == spaceSize
