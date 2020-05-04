# COMOKIT-HPC
ToolKit to launch COMOKIT on a HPC (primary SLURM job scheduler x COMOKIT OpenJDK8)

# How to use :

## Genere XML

```
$ python generateMultipleXML.py -h
usage: generateMultipleXML.py [-h] [-r INT] [-s INT] [-f INT] [-o STR] -xml <experiment name>
                              /path/to/file.gaml /path/to/file.xml

optional arguments:
  -h, --help            show this help message and exit
  -r INT, --replication INT
                        Number of replication for each paramater space
  -s INT, --split INT   Split XML file every S replications
  -f INT, --final INT   Final step for simulations
  -o STR, --output STR  Path to folder where save output CSV
  -xml <experiment name> /path/to/file.gaml /path/to/file.xml
                        Classical xml arguments
```

**Example**
```
$ python generateMultipleXML.py -xml "Headless" ~/Documents/COMOKIT/Models/COMOKIT/Experiments/Physical\ Interventions/Significance\ of\ Wearing\ Masks.gaml /tmp/headless/mask.xml -r 1000 -s 36 -f 5000
```

## Genere SLURM configuration file

```
$ python generateJavaConfFile.py -h
usage: generateJavaConfFile.py [-h] [-n] [-c] [-f] [-x] -g  [-o]

optional arguments:
  -h, --help      show this help message and exit
  -n , --node     Number of nodes to dispatch your exploration on
  -c , --core     Number of cores per node
  -f , --folder   Absolute path to folder where your XML are stored (will gather EVERY! XML file)
  -x , --xml      Absolute path to your XML (/path/to/your/headlessExplo.xml)
  -g , --gama     Absolute path to GAMA headless script (/path/to/your/gama/headless/gama-
                  headless.sh)
  -o , --output   Path to your saved conf file (default: "./gama-headless.conf")
```

**Example**
```
$ python generateJavaConfFile.py -f /tmp/headless -g ~/.local/share/GAMA_Continuous_Linux/headless/gama-headless.sh -n 50 -c 36
```

# Build with
- Python 3 (tested with 3.8.2)