# %%
import numpy as np
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, depolarizing_error
from qiskit.quantum_info import random_quantum_channel


# %%
# def get_noise(model, p, qubits):
#     """
#     Returns noise models and channels.

#     TODO: extend this description.

#     Parameters:
#          model: ???
#          p: ???
#          qubits: ???
#     """
#     if model == 'dep':
#         chan = depolarizing_error((4 * p) / 3, qubits)
#     elif model == 'flip':
#         chan = pauli_error([('X', p), ('I', 1 - p)])
#     noise_model = NoiseModel()
#     noise_model.add_all_qubit_quantum_error(chan, "measure")

#     return chan


def rand_chan_list(num_rand_chan, qchan, rank):
    """ 
    Save a list of random quantum channels. 

    Parameters:
    -----------
    num_rand_chan: number of random channels as an input.
    qchan: dimension (qubits) of the channel
    rank: rank of the generated channels
    ################
    returns:
    -------
    list of random quantum channels of 1 <= rank <= 2**(2*qchan)+1
    """

    chan_list = []
    chan_list_fname = 'data/rand_chan_{}_qubits_{}_rank'.format(qchan, rank)

    print("[INFO] Generating ", num_rand_chan, " channels (", qchan, "qubits, rank",
          rank, ")")

    for i in range(1, num_rand_chan + 1):
        rand_chan = random_quantum_channel(2 ** qchan, 2 ** qchan, rank=rank).data
        chan_list.append(rand_chan)

    np.save(chan_list_fname, chan_list)
    print("[INFO] Saving in", chan_list_fname, '.npy')


# %%
if __name__ == '__main__':

    # TODO: explain what should be expected from this script - is this for tensor product as well?

    qchan_dims = [1]
    num_rand_chan = 1000
    for qchan in qchan_dims:
        for rank in range(1, 2**(2*qchan)+1):
            rand_chan_list(num_rand_chan, qchan, rank)

    # qchan = 2
    # dm = random_density_matrix(2**qchan, 2**qchan).data
    # x = tensor_product.tensorproduct(dm,dm)
    # print(x.shape)
