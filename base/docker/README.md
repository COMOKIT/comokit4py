# COMOKIT Docker Container

A bundled Docker container with GAMA continuous, the COMOKIT framework and the COMOKIT-HPC scripts 

## Getting Started

These instructions will cover usage information and for the docker container 

### Prerequisities


In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

### Usage

#### Container Parameters

Launching gama-headless

```shell
$ docker run --rm comokit/comokit:latest -help
```

Launching an hpc script (here `generateMultipleXML.py` for example)

```shell
# You have to change the "entrypoint"
docker run --rm --entrypoint=/comokit/hpc/pre-processing/generateMultipleXML.py comokit/comokit:latest -xml ContactRateHumanHeadless /comokit/Experiments/Sensitivity\ Analysis/Sensitivity\ Analysis.gaml /tmp/headless/mask.xml -r 100 -s 36 -f 10
```

If you want full explaination of script commands, see [script's README here](https://github.com/COMOKIT/COMOKIT-HPC/tree/master/scripts)

#### Environment Variables

Same as for the based GAMA Docker

* `gama` - Alias for the GAMA binary
* `gama-headless` - Alias for the `gama-headless.sh` script

<!--
#### Volumes

* `/your/file/location` - File location
-->

#### Useful File Locations

* `/usr/usr/lib/gama` - The continuous version of [GAMA](http://gama-platform.org)

* `/usr/usr/lib/gama/headless/gama-platform.sh` - The helping file to launch [GAMA Headless](http://gama-platform.org/wiki/Headless)

* `/comokit/` - The latest version of [COMOKIT](https://github.com/COMOKIT/COMOKIT-Model/tree/master/COMOKIT)

* `/comokit/hpc/` - The latest version of [COMOKIT-HPC scripts](https://github.com/COMOKIT/COMOKIT-HPC/tree/master/scripts)

## Built With

* GAMA-Platform Continuous - https://github.com/gama-platform/gama/releases/tag/continuous
* COMOKIT-Model - https://github.com/COMOKIT/COMOKIT-Model
* COMOKIT-HPC scripts - https://github.com/COMOKIT/COMOKIT-HPC

## Find Us

* [GitHub](https://github.com/COMOKIT)
* [Docker Hub](https://hub.docker.com/r/comokit/comokit)
* [COMOKIT](http://comokit.org)

<!--
## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
-->

## Authors

* **Arthur Brugiere** - *HPC developer* - [RoiArthurB](https://github.com/RoiArthurB)

See also the list of [contributors](https://github.com/orgs/COMOKIT/people) who participated in this project.

## License

The COMOKIT project is licensed under the GPL-3.0 License - see the [LICENSE.md](https://github.com/COMOKIT/COMOKIT-Model/blob/master/LICENSE) file for details.
The Docker image is licensed under the LGPL-3.0 License - see the [LICENSE.md](https://github.com/COMOKIT/COMOKIT-HPC/blob/master/LICENSE) file for details.
