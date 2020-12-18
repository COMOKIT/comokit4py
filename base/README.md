<!-- PROJECT LOGO -->
<p align="center">
  <h3 align="center">COMOKIT-HPC 🧰</h3>

  <p align="center">
    Fight the COVID-19 with HPC
    <br />
    <a href="https://comokit.org"><strong>Explore the project »</strong></a>
    <br />
    <br />
    <a href="https://github.com/COMOKIT/COMOKIT-HPC/graphs/contributors"><img alt="Contributors" src="https://img.shields.io/github/contributors/COMOKIT/COMOKIT-HPC.svg?style=flat-square" /></a>
    ·
    <a href="https://github.com/COMOKIT/COMOKIT-HPC/issues"><img alt="Issues" src="https://img.shields.io/github/issues/COMOKIT/COMOKIT-HPC.svg?style=flat-square)](https://github.com/COMOKIT/COMOKIT-HPC/issues" /></a>
    ·
    <a href="https://github.com/COMOKIT/COMOKIT-HPC/blob/master/LICENSE"><img alt="LGPL3 License" src="https://img.shields.io/github/license/COMOKIT/COMOKIT-HPC.svg?style=flat-square" /></a>
    <br />
    <a href="https://travis-ci.org/github/COMOKIT/COMOKIT-HPC"><img alt="Travis Build Status" src="https://travis-ci.org/COMOKIT/COMOKIT-HPC.svg?branch=master" /></a>
    ·
    <a href="https://github.com/COMOKIT/COMOKIT-HPC/actions"><img alt="Docker Image CI" src="https://github.com/COMOKIT/COMOKIT-HPC/workflows/Docker%20Image%20CI/badge.svg" /></a>
  </p>
</p>


<!-- ABOUT THE PROJECT -->
## About The Project

You will find many useful ressources to run [COMOKIT](http://comokit.org) in headless on many kind of [HPC](https://en.wikipedia.org/wiki/High-performance_computing)

## Repository

Here's the structure of the repository :

- [`/docker/`](https://github.com/COMOKIT/COMOKIT-HPC/tree/master/docker)
  - Carry the COMOKIT docker image (downloadable [here](https://hub.docker.com/r/comokit/comokit))
- [`/pre-processing/`](https://github.com/COMOKIT/COMOKIT-HPC/tree/master/pre-processing)
  - Scripts to prepare exploring models with [GAMA-Headless](https://gama-platform.github.io/wiki/Headless) and execution with [SLURM](https://slurm.schedmd.com/) Workload Manager
  - Mostly Python 3 scripts
- [`/post-processing/`](https://github.com/COMOKIT/COMOKIT-HPC/tree/master/post-processing)
  - Scripts to gather and exploit data extracted from the exploration
  - Mostly R scripts
- [`/tools/`](https://github.com/COMOKIT/COMOKIT-HPC/tree/master/tools)
  - Several small scripts to fix some commun problems with the project/headless usage
  - The doc will only be in the header of the file

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

The COMOKIT project is distributed under the GPL-3.0 License. See [LICENSE](https://github.com/COMOKIT/COMOKIT-Model/blob/master/LICENSE) for more information.

These scripts are distributed under the LGPL-3.0 License. See [LICENSE](https://github.com/COMOKIT/COMOKIT-HPC/blob/master/LICENSE) for more information.
