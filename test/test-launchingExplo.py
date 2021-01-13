import comokit4py
import os

#
#	Setup GAMA
#	cf. test-gama.py
#
gamaPath = "../../../../.local/share/GAMA_1.8.1_Linux"
gamaPathHeadless = os.path.join(gamaPath,"headless/gama-headless.sh")

gama = comokit4py.Gama(gamaPathHeadless)

#
#	Setup GAMA Exploration
#	cf. test-gamaExp.py
#
explo = comokit4py.GamaExploration(experimentName = "Headless", gamlFile = "/home/roiarthurb/Documents/COMOKIT/Model/COMOKIT/Experiments/Physical Interventions/Significance of Wearing Masks.gaml", replication = 4, final = 5, experimentPerXML  = 2)
explo.calculatesExperimentSpace()

#
#	Setup GAMA Exploration Workspace
#
ws = comokit4py.Workspace(gama, explo, "./out", True)

print("Verify all :", ws.verifyAll())

ws.generateNeededForExploration()
ws.runGamaHeadless(cores = 4)

print("Exploration done")

