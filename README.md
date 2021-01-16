![PyPI - Package Version](https://img.shields.io/pypi/v/comokit4py)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/comokit4py)
![PyPI - Downloads](https://img.shields.io/pypi/dd/comokit4py)

![GitHub](https://img.shields.io/github/license/COMOKIT/comokit4py)
![Maintenance](https://img.shields.io/maintenance/yes/2021)

# comokit4py

comokit4py is a Python3 library for easily explore [COMOKIT](https://comokit.org) models, and process outputted data, on your laptop or an HPC in a few Python lines.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install comokit4py.

```bash
pip install comokit4py
```

## Usage example

```python
import comokit4py

# Prepare GAMA (COMOKIT base software)
gama = comokit4py.Gama("~/.local/share/GAMA_1.8.1_Linux/headless/gama-headless.sh")

# Prepare exploration
explo = comokit4py.GamaExploration(experimentName = "Headless", 
	gamlFile = "~/Documents/COMOKIT/Model/COMOKIT/Experiments/Physical Interventions/Significance of Wearing Masks.gaml", 
	replication = 2, final = 5)
explo.calculatesExperimentSpace()

# Setup the exploration's workspace
ws = comokit4py.Workspace(gama, explo, "./out", True)

# Launch exploration
ws.runGamaHeadless(log = True, cores = 4)
```

The full library documentation is here : [https://comokit.github.io/comokit4py/](https://comokit.github.io/comokit4py/)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[LGPL-2.1 License](https://github.com/COMOKIT/comokit4py/blob/main/LICENSE)