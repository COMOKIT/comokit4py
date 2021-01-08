import comokit4py
import os

gamaPath = "../../../../.local/share/GAMA_1.8.1_Linux"
gamaPathHeadless = os.path.join(gamaPath,"headless/gama-headless.sh")

gama = comokit4py.Gama(gamaPathHeadless)

exitCode = 0
print("[Script path]", "\t", os.path.abspath(gamaPathHeadless) == gama.getPathToHeadlessScript())
exitCode = 1 if not (os.path.abspath(gamaPathHeadless) == gama.getPathToHeadlessScript()) else exitCode

print("[Base Dir]", "\t", os.path.abspath(gamaPath) == gama.getBaseDir())
exitCode = 1 if not (os.path.abspath(gamaPath) == gama.getBaseDir()) else exitCode

print("[Version]", "\t", "1.8.1" == gama.getVersion())
exitCode = 1 if not ("1.8.1" == gama.getVersion()) else exitCode

print("[Memory]", "\t", "4096m" == gama.getMemory())
exitCode = 1 if not ("4096m" == gama.getMemory()) else exitCode

gama.setMemory("4g")
print("[Memory changed]", "4g" == gama.getMemory())
exitCode = 1 if not ("4g" == gama.getMemory()) else exitCode

os._exit(exitCode)