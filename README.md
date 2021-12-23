# variational channel fidelity estimation
Source code used for variational quantum fidelity estimation for quantum channels.

## Quick start

### 

1. Run `generator.py` to produce a sample of random channels. By default 1000 channels are generated.
2. Run `vqcd_optimization.py n`, where `n` is the index of the channel generated in the previous steps.
3. Run `vqcd_all_chan.py`, to generate and save the average error in fidelity estimation with respect to rank of the state.
4. Run `vqcd_single_chan.py` to generate and save the error in fidelity estimation for the lowest error channel. Note to generate the lowest error quantum channel run `lowest_error_channel.py`, which saves the channel number with lowest error.
3. Run `vqcd_plot.py` to generate and save the plots. 

## Description

This repository contains source code for running diagonalization procedure as well as to estimate fidelity (error in fidelity estimation) for `1` and `2` qubit channels.

## Code for quantum channels 

The main folder contains the following files:

* `generate.py` for generating random channels. The generated channels are saved in the `data` subdirectory,

* `vqcd_main_funcs.py` contains the main subroutines of the diagonalization and fidelity estimation algorithm as follows 
  * `cost_func` cost function evaluation, 
  * `eig_info` inferred eigenvalues generation and 
  * `trun_output` (truncated fidelity bounds estimation) functions.

* `vqcd_secondary_funcs.py` contains secondary subroutines as follows
  * `jamilchoi` generates Choi–Jamiołkowski (JC) state of any dimension quantum channel,
  * `purity_before_diag` gives the purity of the state before diagonalization,
  * `maximum_likelihood` performs maximum-likelihood to avoid negative eigenvalues.

* `vqcd_optimization.py n`, where `n` is the index of the channel generated (if no `n` provided then the index by default is `0`) to run optimization procedure for random quantum channels, by default the optimized angles are saved in `data/opt_ang_test` subfolder,

* `vqcd_all_chan.py` for finding the average error in fidelity estimation (by default the channel number set to `1000`), by default the average error for each channel are saved in `data/fid_plot_data_test` subfolder,

* `vqcd_single_chan.py` for finding the convergence of fidelity with rank of the state for a particular quantum channel, by default the average error for each channel are saved in `data/fid_plot_data_test` subfolder,

* `vqcd_plot.py` for plotting the results and contains two subroutines as follows
  * `average_fidelity` returns plot for average fidelity estimation error for a defined total number of channels,
  * `single_chan_fidelity` returns plot for a single channel depicting truncated fidelity bound in respect with rank of the JC state.
Plots are saved in `plot` subdirectory


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
    
    !pip install qiskit==0.18.2

