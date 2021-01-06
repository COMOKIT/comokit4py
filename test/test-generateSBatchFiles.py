import argparse
from comokit4py import generateSBatchFiles

if __name__ == '__main__':

	# 0 _ Get/Set parameters
	# 
	parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options]')

	#	SBATCH settings
	parser.add_argument('-s', '--submission', metavar='', help="Total of submission on SLURM", default=1, type=int)
	parser.add_argument('-S', '--maxSubmission', metavar='', default=1, type=int, help="Max number of active submission on SLURM")
	parser.add_argument('-n', '--nodes', metavar='', help="Number of nodes to dispatch your exploration on", default=1, type=int)
	parser.add_argument('-T', '--cpuPerTask', metavar='', help="Number of core allocated to a single task", default=1, type=int)
	parser.add_argument('-c', '--core', metavar='', help="Number of cores per node", default=1, type=int)
	parser.add_argument('-t', '--time', metavar='', help="Time (in hour) for your job", default=1, type=int)
	parser.add_argument('-d', '--delay', metavar='', help="Delay in between launching headless (ex. 2s, 3m, 4h, 5d)", required=False)
	#	GAMA Headless settings
	parser.add_argument('-f', '--folder', metavar='', help="Path to folder where your XML are stored (will gather EVERY! XML file)", type=str, required=True)
	parser.add_argument('-g', '--gama', metavar="", help = 'Path to GAMA headless script (/path/to/your/gama/headless/gama-headless.sh)', type=str, required=False, default="../../GAMA/headless/gama-headless.sh")
	parser.add_argument('-F', '--outputFolder', metavar="", help='Path to folder where GAMA will write simulation\'s console output (default: "./sbatchUtilities/tmp/.gama-output")', type=str, default="./sbatchUtilities/tmp/.gama-output")
	#	Script settings
	parser.add_argument('-o', '--output', metavar="", help='Path to folder where save every needed sbatch files (default: "./sbatchUtilities")', type=str, default="./sbatchUtilities")
	parser.add_argument('--EDF', action='store_true', help='Will add extra parameters for EDF collaboration')
	parser.add_argument('-A', action='store_true', help='Will turn every path in absolute path')

	args = parser.parse_args()

	# 1 _ Setup environment to be sure to launch
	#
	print("=== Prepare everything")
	xmlPath = generateSBatchFiles.setupGamaEnv(args.gama, args.output, args.outputFolder, args.A, args.folder)
	if xmlPath != "":
		print("\tDone !")

	# 2 _ Create SBatch first script
	#
	print("=== Generate " + args.output + "/sbatch_array.sh file")
	if generateSBatchFiles.genSbatchArray(args.output, args.submission, args.maxSubmission, args.nodes, args.cpuPerTask, args.core, args.time, args.EDF):
		print("\tSaved !")

	# 3 _ Create SBatch second script
	#
	print("=== Generate " + args.output + "/vague.cnf file")
	if generateSBatchFiles.genVague(args.output, args.nodes, args.cpuPerTask, args.core):
		print("\tSaved !")

	# 4 _ Create gama headless launching script
	#
	print("=== Generate " + args.output + "/launch_pack_8.sh file")
	if generateSBatchFiles.genLaunchPack(args.gama, args.output, args.outputFolder, xmlPath, args.nodes, args.cpuPerTask, args.core, args.delay):
		print("\tSaved !")