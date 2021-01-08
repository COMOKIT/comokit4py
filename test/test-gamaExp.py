import comokit4py
import os

explo = comokit4py.GamaExploration(experimentName = "Headless", gamlFile = "/home/roiarthurb/Documents/COMOKIT/Model/COMOKIT/Experiments/Physical Interventions/Significance of Wearing Masks.gaml", replication = 1, final = 5000, experimentPerXML  = 8)
explo.calculatesExperimentSpace()

#
#	TESTS
#

exitCode = 0

explo.getExperimentName
print("[Exp Name]", "\t", explo.getExperimentName == "Headless")
exitCode = 1 if not (os.path.abspath(gamaPathHeadless) == gama.getPathToHeadlessScript()) else exitCode

print("[Gaml File]", "\t", explo.getGamlFile() == os.path.abspath("/home/roiarthurb/Documents/COMOKIT/Model/COMOKIT/Experiments/Physical Interventions/Significance of Wearing Masks.gaml"))

print("[XML out]", "\t", explo.getXmlOutputName() == "headless.xml")

print("[Replicat]", "\t", explo.getReplication() == 1)

print("[Xml / Exp]", "\t", explo.getExperimentPerXML() == 8)

print("[Final stp]", "\t", explo.getFinal() == 5000)

print("[End cond]", "\t", explo.getUntil() == "")

print("[Start seed]", "\t", explo.getSeed() == 0)

print("[Param combi]", "\t", len(explo.getParametersList()) == 121)

print("[With rep]", "\t", len(explo.getExperimentSpace()) == 121)

os._exit(exitCode)