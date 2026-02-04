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
X. Li and V. Stolyarov, "PulSKASim: A Pulsar Simulator for SKA-Scale Interferometric Observations", Astronomical Data Analysis Software and Systems (ADASS) XXXV, 2025.

## License

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
