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
explo = comokit4py.GamaExploration(experimentName = "Headless", gamlFile = "/home/roiarthurb/Documents/COMOKIT/Model/COMOKIT/Experiments/Physical Interventions/Significance of Wearing Masks.gaml", replication = 2, final = 5)
explo.calculatesExperimentSpace()

#
#	Setup GAMA Exploration Workspace
#
ws = comokit4py.Workspace(gama, explo, "./out", True)

print("Verify all :", ws.verifyAll())

ws.generateNeededForExploration()
#ws.runGamaHeadless(log = False, cores = 4)

print("Exploration done")

ws.prepareProcessedOutput(quartile = True, startDate = [2020, 1, 24], startPolicyDate = [2020, 3, 17], endPolicyDate = [2020, 5, 11])

p = ws.rawOutputProcessing()

ws.generateCsv(output = p)
ws.generatePng(title = "Title", output = p)
print("=== End ===")