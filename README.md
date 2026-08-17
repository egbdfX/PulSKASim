# PulSKASim: A Pulsar Simulator for SKA-Scale Interferometric Observations
This simulator is designed for large-scale radio interferometers. Please see our paper in Section [Reference](https://github.com/egbdfX/PulSKASim/tree/main#reference) for more information.

## Run flux generator
The flux simulation script **flux_generator.py** is written in Python, with an equivalent MATLAB implementation provided as **flux_simul.m**.

## Run pyuvsim simulations

The interferometric simulation script **pyuvsim_simul.py** uses **pyuvsim** which requires to clone [pyuvsim](https://github.com/RadioAstronomySoftwareGroup/pyuvsim) and to install it with **pip**.
The script **pyuvsim_simul.py** starts **scripts/run_param_pyuvsim.py** that is a part of pyuvsim package (commit **6e9cd2a**). MPI package (e.g. **openmpi**) is also required to provide **mpirun**.

## Run OSKAR simulations

The interferometric simulation script **oskarsim.py** requires **OSKAR** python infrastructure installed, see [OSKAR repository](https://github.com/OxfordSKA/OSKAR).

## Reference

**When referencing this code, please cite our related paper:**

X. Li and V. Stolyarov, "[PulSKASim: A Pulsar Simulator for SKA-Scale Interferometric Observations](https://arxiv.org/abs/2603.04593)", Astronomical Data Analysis Software and Systems (ADASS) XXXV, 2025.

## License

Shield: [![BSD 3-Clause][bsd-3-shield]][bsd-3]

This work is licensed under a
[BSD 3-Clause License][bsd-3].

[bsd-3]: https://opensource.org/licenses/BSD-3-Clause
[bsd-3-shield]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
