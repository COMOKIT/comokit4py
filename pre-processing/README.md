# COMOKIT-HPC - Pre-Processing
ToolKit to launch COMOKIT on a HPC (primary SLURM job scheduler x COMOKIT OpenJDK8)

# How to use :

## Genere XML

```
$ python3 generateMultipleXML.py -h
usage: $ python3 generateMultipleXML.py [options] -f INT -xml <experiment name> /path/to/file.gaml /path/to/file.xml

optional arguments:
  -h, --help            show this help message and exit
  -r INT, --replication INT
                        Number of replication for each paramater space (default: 1)
  -s INT, --split INT   Split XML file every S replications (default: 1)
  -o STR, --output STR  Path to folder where save output CSV (default: "../../batch_output")
  -u STR, --until STR   Stop condition for the simulations (default: "world.sim_stop()"
  -S INT, --seed INT    Starting value for seeding simulation (default: 0)
  -f INT, --final INT   Final step for simulations
  -xml <experiment name> /path/to/file.gaml /path/to/file.xml
                        Classical xml arguments
```

**Example**
```
$ python3 generateMultipleXML.py -xml "Headless" ~/Documents/COMOKIT-Model/COMOKIT/Experiments/Physical\ Interventions/Significance\ of\ Wearing\ Masks.gaml /tmp/headless/mask.xml -r 1000 -s 36 -f 5000
Total number of parameters detected : 2
Total number of possible combinaison : 121
  Replications : 1000
  Number of exp in file : 36
  Final step : 5000
=== Start generating XML file :
(every dot will be a simulation with all the replications created)
.........................................................................................................................
=== Start saving XML file

=== Done ;)

$ ls -la /tmp/headless | head
total 189212
drwxr-xr-x  2 roiarthurb roiarthurb 302580 13 mai   09:55 .
drwxrwxrwt 20 root       root         1040 13 mai   10:03 ..
-rw-r--r--  1 roiarthurb roiarthurb  26357 13 mai   10:16 mask-0.xml
-rw-r--r--  1 roiarthurb roiarthurb   6459 13 mai   09:31 mask-10000.xml
-rw-r--r--  1 roiarthurb roiarthurb   6459 13 mai   09:31 mask-10001.xml
-rw-r--r--  1 roiarthurb roiarthurb   6459 13 mai   09:31 mask-10002.xml
-rw-r--r--  1 roiarthurb roiarthurb   6459 13 mai   09:31 mask-10003.xml
-rw-r--r--  1 roiarthurb roiarthurb   6459 13 mai   09:31 mask-10004.xml
-rw-r--r--  1 roiarthurb roiarthurb   6459 13 mai   09:31 mask-10005.xml
```

## Genere SLURM SRUN configuration file

```
$ python3 generateJavaConfFile.py -h 
usage: $ python3 generateJavaConfFile.py [options]

optional arguments:
  -h, --help            show this help message and exit
  -n , --node           Number of nodes to dispatch your exploration on
  -c , --core           Number of cores per node
  -f , --folder         Path to folder where your XML are stored (will gather EVERY! XML file)
  -x , --xml            Path to your XML (/path/to/your/headlessExplo.xml)
  -g , --gama           Path to GAMA headless script (/path/to/your/gama/headless/gama-headless.sh)
  -F , --outputFolder   Path to folder where GAMA will write simulation's console output
  -o , --output         Path to your saved conf file (default: "./gama-headless.conf")
```

**Example**
```
$ python generateJavaConfFile.py -f /tmp/headless -g ~/.local/share/GAMA_Continuous_Linux/headless/gama-headless.sh -n 50 -c 36
```

## Genere SLURM SBatch-Array configuration file

```
python generateSBatchFiles.py -h
usage: $ python3 generateSBatchFiles.py [options]

optional arguments:
  -h, --help            show this help message and exit
  -s , --submission     Total of submission on SLURM
  -S , --maxSubmission 
                        Max number of active submission on SLURM
  -n , --nodes          Number of nodes to dispatch your exploration on
  -T , --cpuPerTask     Number of core allocated to a single task
  -c , --core           Number of cores per node
  -t , --time           Time (in hour) for your job
  -f , --folder         Path to folder where your XML are stored (will gather EVERY! XML file)
  -g , --gama           Path to GAMA headless script (/path/to/your/gama/headless/gama-headless.sh)
  -F , --outputFolder   Path to folder where GAMA will write simulation's console output (default: "/tmp/.gama-output")
  -o , --output         Path to folder where save every needed sbatch files (default: "./sbatchUtilities")

  --EDF                 Will add extra parameters for EDF collaboration
  -A                    Will turn every path in absolute path
```

**Example**
```
$ python3 generateSBatchFiles.py -g /tmp/fakeGama.sh -f /tmp/headless -s 27 -S 6 -n 16 -T 1 -c 36 --EDF -A
=== Prepare everything
=== Generate /home/roiarthurb/Documents/COMOKIT-HPC/pre-processing/sbatchUtilities/sbatch_array.sh file
  Saved !
=== Generate /home/roiarthurb/Documents/COMOKIT-HPC/pre-processing/sbatchUtilities/vague.cnf file
  Saved !
=== Generate /home/roiarthurb/Documents/COMOKIT-HPC/pre-processing/sbatchUtilities/launch_pack_8.sh file
  Saved !

$  cat ./sbatchUtilities/*
-- ./sbatchUtilities/launch_pack_8.sh
#!/bin/bash

id_mask=$(( $SLURM_ARRAY_TASK_ID * 576 + $1 ))
if [ ! -f  /tmp/headless/t.xml-${id_mask}.xml ]; then echo "le fichier mask-${id_mask}.xml est absent (queue de distrib?)"; exit 2; fi
/tmp/fakeGama.sh /tmp/headless/t.xml-${id_mask}.xml /tmp/.gama-output

-- ./sbatchUtilities/sbatch_array.sh
#!/bin/bash
srun --multi-prog /home/roiarthurb/Documents/COMOKIT-HPC/pre-processing/sbatchUtilities/vague.cnf
#-------------------------------------------------------------------------------
#
# Batch options for SLURM (Simple Linux Utility for Resource Management)
# =======================
#
#SBATCH --array=0-26%6
#SBATCH --nodes=16
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=576
#SBATCH --ntasks-per-node=36
#SBATCH --time=1:00:00
#SBATCH --job-name=COMOKIT
#SBATCH --exclusive
#SBATCH --partition=cn
#SBATCH --wckey=IRD:GAMA
#
#-------------------------------------------------------------------------------

# Change to submission directory
if test -n ${1} ; then cd ${1} ; fi

-- ./sbatchUtilities/vague.cnf
0-575 /home/roiarthurb/Documents/COMOKIT-HPC/pre-processing/sbatchUtilities/launch_pack_8.sh %t          
```

# Build with
- [Linux System](https://www.linux.com/what-is-linux/) (Debian & Manjaro)
- [Python 3](https://www.python.org/downloads/) (tested with 3.8.2) 
- [SLURM](https://slurm.schedmd.com/)

## Authors

* **Arthur Brugiere** - *HPC developer* - [RoiArthurB](https://github.com/RoiArthurB)

See also the list of [contributors](https://github.com/orgs/COMOKIT/people) who participated in this project.
