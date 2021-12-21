# variational channel fidelity
Source code used for variational quantum fidelity estimation for quantum channels.

## Quick start

### 

1. Run `generator.py` to produce a sample of random channels. By default 1000 channels are generated.
2. Run `optimize.py n`, where `n` is the index of the channel generated in the previous steps.
3. Calculations of channel distinguishability

## Description

This repository contains source code for running diagonalization procedure for quantum states and quantum channels. The
code is divided into two parts.

## Code for quantum channels 

The main folder contains the following files:
* `generate.py` for generating random channels. The generated channels are saved in the `data` subdirectory,
* `optmize.py` for running optimization procedure for random quantum channels,
* `VQCD_calculation.py` for finding the error in eigenvalue/finding operation distance,
* `VQCD_plot.pl` for plotting the results. Plots are saved in `plot` subdirectory.

## Code for quantum states

Folder `src/state` contains the following files

* `generator.py` for generating samples of random quantum states,
* `optimize.py` for optimizing random states,
* for finding the error 
  * in eigenvalue in real device `real_dev_eigenvals_list_rand_state.py`,
  * using adopted noise/simulator `eigenvals_list_rand_state.py`,
* For plotting the data `eig_error_plot.py`,
* `plots` folder for saving plots
* `state_data` folder for storing data.


## Folder `text` 
This folder is a placeholder for the preprint files.

## License

This code can be distributed under the Apache License.

## Installation and requirements

Python scripts in this repository have been tested with
* qiskit (0.18.2)
* numpy (1.21.2)
* scipy (1.7.1)

To install the recent version of Qiskit run 
    
    pip install qiskit

