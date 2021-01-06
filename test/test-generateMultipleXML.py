import argparse, os
from comokit4py import generateMultipleXML

if __name__ == '__main__':

	# 0 _ Get/Set parameters
	# 
	parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options] -f INT -xml <experiment name> /path/to/file.gaml /path/to/file.xml')
	parser.add_argument('-r', '--replication', metavar='INT', help="Number of replication for each paramater space (default: 1)", default=1, type=int)
	parser.add_argument('-s', '--split', metavar='INT', help="Split XML file every S replications (default: 1)", default=-1, type=int)
	parser.add_argument('-o', '--output', metavar='STR', help="Relative path from GAML file to folder where save output CSV (default: \"../../batch_output\" => /path/to/COMOKIT/batch_output)", default="../../batch_output", type=str)
	parser.add_argument('-u', '--until', metavar='STR', help="Stop condition for the simulations (default: \"world.sim_stop()\"", default="", type=str)
	parser.add_argument('-S', '--seed', metavar='INT', help="Starting value for seeding simulation (default: 0)", default=0, type=int)	
	parser.add_argument('-f', '--final', metavar='INT', help="Final step for simulations", default=-1, type=int,  required=True)
	parser.add_argument('-xml', metavar=("<experiment name>", "/path/to/file.gaml", "/path/to/file.xml"), nargs = 3, help = 'Classical xml arguments', required=True)
	args = parser.parse_args()

	# 0 _ Set used variables
	# 
	expName, gamlFilePath, xmlFilePath = args.xml
	parametersList = []

	# 1 _ Gather all parameters
	# 
	allParamValues, parametersList = generateMultipleXML.generateExperimentUniverse(gamlFilePath)

	# 1.1 _ Inform about whole parameters
	# 
	print("Total number of possible combinaison : " + str(len(allParamValues)))
	print("\tReplications : " + str(args.replication))
	print("\tNumber of exp in file : " + (str(args.split) if args.split != -1 else 'All') )
	print("\tFinal step : " + str(args.final))

	# 2 _ Generate XML
	# 
	print("=== Start generating XML files...\n")

	print("\tNote : Real total number of simulation is " + str(len(allParamValues) * args.replication))

	if generateMultipleXML.createXmlFiles(expName, gamlFilePath, allParamValues, parametersList, xmlFilePath, args.replication, args.split, os.path.abspath(os.path.split(gamlFilePath)[0] + "/" + args.output), args.seed, args.final, args.until) :
		print("\n=== Done ;)")
	else:
		print("\n=== Error :(")