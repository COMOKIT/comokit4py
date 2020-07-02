#!/bin/sh

##################################################
## Bash script to avoid mistakes while launching on EDF's HPC
## $ sh ./edf.sh <id>
#
##################################################
## Author: RoiArthurB
## Copyright: Copyright 2020, COMOKIT, COMOKIT-HPC
## Licence: LGPL 3.0
## Version: 1.0.0
## Maintainer: RoiArthurB
##################################################

#
#	Generative commands
#

#
#	generateXML <experiment name> <file path from /COMOKIT/Experiments>
###
function generateXML {
	echo "%%% Generating XML for experiment $1"
	reps=${3:-1000}
	cyclend=${4:-5000}
	python3 "$( dirname "${BASH_SOURCE[0]}" )"/../pre-processing/generateMultipleXML.py -r "$reps" -s 8 -f "$cyclend$ -xml $1 "$( dirname "${BASH_SOURCE[0]}" )"/../../COMOKIT/Experiments/"$2" "$( dirname "${BASH_SOURCE[0]}" )"/../../XML/mask.xml
}

#
#	Same as generateXML but with 1 simulation per XML file
###
function generateXML_bigSimulation {
	reps=${3:-100}
	cyclend=${4:-8000}
	python3 "$( dirname "${BASH_SOURCE[0]}" )"/../pre-processing/generateMultipleXML.py -r "$reps" -s 1 -f "$cyclend$ -xml $1 "$( dirname "${BASH_SOURCE[0]}" )"/../../COMOKIT/Experiments/"$2" "$( dirname "${BASH_SOURCE[0]}" )"/../../XML/mask.xml
}

#
#	generateSBatch <no parameter>
###
function generateSBatch {
	echo "%%% Total of XML : $(ls -l "$( dirname "${BASH_SOURCE[0]}" )"/../../XML | wc -l)"
	echo ""
	echo "%%% Generate SBatch scripts"
	python3 "$( dirname "${BASH_SOURCE[0]}" )"/../pre-processing/generateSBatchFiles.py -g "$( dirname "${BASH_SOURCE[0]}" )"/../../GAMA/headless/gama-headless.sh -f "$( dirname "${BASH_SOURCE[0]}" )"/../../XML -s 27 -S 6 -n 16 -T 1 -c 36 --EDF -A
}

#
#	MAIN
#
if [ ! -d "$( dirname "${BASH_SOURCE[0]}" )/../../XML" ]; then
	echo "%%% Creating XML folder"
	mkdir "$( dirname "${BASH_SOURCE[0]}" )"/../../XML
else
	echo "%%% Cleaning XML folder"
	rm -fr "$( dirname "${BASH_SOURCE[0]}" )"/../../XML/*
fi
	
case "$1" in
"1")	# Damien sensibility
	generateXML HeadlessComparison Sensitivity\ Analysis/Comparison\ With\ and\ Without\ Environmental\ Transmission.gaml
    generateXML ContactRateHumanHeadless Sensitivity\ Analysis/Sensitivity\ Analysis.gaml
 
    generateSBatch
    ;;
"2")	# Kevin Camps explorations
	generateXML_bigSimulation HeadlessContactTracing ../../COMOKIT-Camps/models/Experiments/ContactTracing.gaml
	generateXML_bigSimulation HeadlessNoPolicy ../../COMOKIT-Camps/models/Experiments/No\ Containment.gaml
	generateXML_bigSimulation HeadlessReducingContactHeadlessReducingContact ../../COMOKIT-Camps/models/Experiments/ReducingContact.gaml
	generateXML_bigSimulation HeadlessReducingAndContactTracing ../../COMOKIT-Camps/models/Experiments/ReducingContactAndTracing.gaml

    generateSBatch
    ;;
*)
    echo "=== ERROR ==="
    echo "You should precise which exploration ID you want to generate"
    echo "============="
    exit 2
    ;;
esac
