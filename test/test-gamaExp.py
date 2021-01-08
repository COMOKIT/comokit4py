import comokit4py
import os

explo = comokit4py.GamaExploration(experimentName = "Headless", gamlFile = "/home/roiarthurb/Documents/COMOKIT/Model/COMOKIT/Experiments/Physical Interventions/Significance of Wearing Masks.gaml", replication = 1, final = 5000, experimentPerXML  = 8)
explo.calculatesExperimentSpace()

#
#	TESTS
#

exitCode = 0

print("[Exp Name]", "\t", explo.getExperimentName() == "Headless")
exitCode = 1 if not (explo.getExperimentName == "Headless") else exitCode

print("[Gaml File]", "\t", explo.getGamlFile() == os.path.abspath("/home/roiarthurb/Documents/COMOKIT/Model/COMOKIT/Experiments/Physical Interventions/Significance of Wearing Masks.gaml"))
exitCode = 1 if not explo.getGamlFile() == os.path.abspath("/home/roiarthurb/Documents/COMOKIT/Model/COMOKIT/Experiments/Physical Interventions/Significance of Wearing Masks.gaml") else exitCode

print("[XML out]", "\t", explo.getXmlOutputName() == "headless.xml")
exitCode = 1 if not (explo.getXmlOutputName() == "headless.xml") else exitCode

print("[Replicat]", "\t", explo.getReplication() == 1)
exitCode = 1 if not (explo.getReplication() == 1) else exitCode

print("[Xml / Exp]", "\t", explo.getExperimentPerXML() == 8)
exitCode = 1 if not (explo.getExperimentPerXML() == 8) else exitCode

print("[Final stp]", "\t", explo.getFinal() == 5000)
exitCode = 1 if not (explo.getFinal() == 5000) else exitCode

print("[End cond]", "\t", explo.getUntil() == "")
exitCode = 1 if not (explo.getUntil() == "") else exitCode

print("[Start seed]", "\t", explo.getSeed() == 0)
exitCode = 1 if not (explo.getSeed() == 0) else exitCode

print("[Param combi]", "\t", len(explo.getParametersList()) == 2)
exitCode = 1 if not (len(explo.getParametersList()) == 2) else exitCode

print("[With rep]", "\t", len(explo.getExperimentSpace()) == 121)
exitCode = 1 if not (len(explo.getExperimentSpace()) == 121) else exitCode

os._exit(exitCode)