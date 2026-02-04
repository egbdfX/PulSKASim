# PulSKASim: A Pulsar Simulator for SKA-Scale Interferometric Observations
This simulator is designed for large-scale radio interferometer. Please see our paper in Section [Reference](https://github.com/egbdfX/PulSKASim/tree/main#reference) for more information.
## Run pyuvsim simulations

The simulations script **pyuvsim_simul.py** uses **pyuvsim** which requires to clone [pyuvsim](https://github.com/RadioAstronomySoftwareGroup/pyuvsim) and to install it with **pip**.
The script **pyuvsim_simul.py** starts **scripts/run_param_pyuvsim.py** that is a part of pyuvsim package (commit **6e9cd2a**). MPI package (e.g. **openmpi**) is also required to provide **mpirun**.

## Run OSKAR simulations

The simulation script **oskarsim.py** requires **OSKAR** python infrastructure installed, see [OSKAR repository](https://github.com/OxfordSKA/OSKAR).

## Reference
