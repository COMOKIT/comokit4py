import argparse, multiprocessing
from comokit4py import comokit2png

if __name__ == '__main__':
    # 0 _ Get/Set parameters
    #
    parser = argparse.ArgumentParser(usage='$ python3 %(prog)s [options]')

    # Files
    parser.add_argument('-i', '--inputFolder', metavar="", help='Path to folder where are saved all the COMOKIT CSV files from explorations (default: "./batch_output")', type=str, default="./batch_output")
    parser.add_argument('-o', '--outputImg', metavar="", help='Where to save output graph (default: "./out" =generate=> "./out[GeneratedNumber].png")', type=str, default="./out")
    parser.add_argument('-e', '--experimentName', metavar="", help='Name of the experiment (if you have several in a same folder)', type=str, default="")
    parser.add_argument('-r', '--replication', metavar='', help="Number of replication per value set (default: 1)", default=1, type=int)

    # PNG
    parser.add_argument('-t', '--title', metavar="", help='Graph title (default: [disabled])', type=str, default="")
    parser.add_argument('-V', '--variance', action='store_true', help='Process min/max with variance')
    parser.add_argument('--csv', action='store_true', help='Save output as CSV file')
    #parser.add_argument('-p', '--plotRow', metavar="", help='Number of line to display graphs (default: 3)', type=int, default=3)
    parser.add_argument('-S', '--displayStep', metavar='', help="Change x index scale in png (default: 24 -> day)", default=24, type=int)
    parser.add_argument('-m', '--median', action='store_true', help='Display median curve in graph')
    parser.add_argument('-Q', '--quartile', action='store_true', help='Display quartile curves in graph (override median option)')

    parser.add_argument('-d', '--startDate', metavar=("YYYY", "MM", "DD"), nargs = 3, help = 'Set starting real date in PNG x axis')
    parser.add_argument('-p', '--startPolicy', metavar=("YYYY", "MM", "DD"), nargs = 3, help = 'Set starting policy grey area in PNG (needs --startDate and --endPolicy)')
    parser.add_argument('-P', '--endPolicy', metavar=("YYYY", "MM", "DD"), nargs = 3, help = 'Set starting policy grey area in PNG (needs --startDate and --startPolicy)')

    # Other
    parser.add_argument('-q', '--quiet', action='store_true', help='Disable verbose mode')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable extra verbose')
    parser.add_argument('-vv', '--extraVerbose', action='store_true', help='Enable even more extra verbose')
    parser.add_argument('-c', '--cores', metavar='', help="Number of core to use (default: max number of cores)", default=multiprocessing.cpu_count(), type=int)
    parser.add_argument('-s', '--stepTo', metavar='', help="Compile several steps in one (default: 1 -> disable)", default=1, type=int)

    # Magic
    parser.add_argument('--azure', action='store_true', help='Tweak display for COMOKIT-Azure purpose')

    args = parser.parse_args()

    # Apply predefined tweaks
    # without overriding potentially already set
    if args.azure:
        if not args.quiet:
            print("=== Apply missing parameter for Azure project ===")
        if not args.startDate:
            args.startDate = [2020, 1, 24]
            if not args.quiet:
                print("\tSet --startDate", args.startDate)
        if not args.startPolicy:
            args.startPolicy = [2020, 3, 17]
            if not args.quiet:
                print("\tSet --startPolicy", args.startPolicy)
        if not args.endPolicy:
            args.endPolicy = [2020, 5, 11]
            if not args.quiet:
                print("\tSet --endPolicy", args.endPolicy)
        if args.replication == 1: # Default value
            args.replication = 50
            if not args.quiet:
                print("\tSet --replication", args.replication)
        if not args.quiet:
            print("=== Done ===\n")

    if args.extraVerbose:
        args.verbose = True

    if args.verbose:
        print("\n=== Starting script ===")

    # 1 _ Gathering COMOKIT datasets
    #
    CSVs = comokit2png.gatheringCSV(batch_path = args.inputFolder, experimentName = args.experimentName)
    if args.verbose:
        print("=== End gathering CSVs ===")

    # 2.1 _ Prepare variables/functions for processing
    #
    output_name  = ["Susceptible", "Recovered", "Presymptomatic", "Asymptomatic", "Symptomatic", "Need hospital", "Need ICU", "Death"]
    output_color = ["g", "b", "olive", "lightgreen", "y", "orange", "r", "m"]

    # 2.2 _ Launch processing
    #
    if not args.quiet:
        print("Start thread processing...")
        if args.verbose:
            print("= Using " + str(args.cores) + " cores on " + str(multiprocessing.cpu_count()) + " availables")

    output = comokit2png.multithreadCsvProcessing(CSVs, output_name, args.stepTo, args.replication, args.cores, args.quartile, args.median, args.variance)

    if args.verbose:
        print("Array form : ", len(output), "x", len(output[0]), "x", len(output[0][0]))
        if args.extraVerbose:
            print("Quick view of some processed data :")
            print(output[0][:3])
        print("Processed " + str(len(output[0])) + " days")

    # 2.3 _ Save output CSV
    # 
    if args.csv:
        saved = comokit2png.saveToCSV(output, output_name, args.outputImg)
        if not args.quiet and saved:
            print("CSV file saved as : " + args.outputImg + '.csv')

    # 3 _ Generating image
    #

    if not args.quiet:
        print("Creating plot...")

    col_name = comokit2png.generateColumnName(args.quartile, args.median)

    comokit2png.savePngGraphs(output = output, col_name = col_name, output_color = output_color, outputImgName = args.outputImg, output_name = output_name, displayStep = args.displayStep, title = args.title, quartile = args.quartile, median = args.median, stepTo = args.stepTo, startDate = args.startDate, startEpidemyDate = args.startPolicy, endEpidemyDate = args.endPolicy)

    if not args.quiet:
        print("Output image saved as : " + args.outputImg + '.png')