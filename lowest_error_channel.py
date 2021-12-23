from vqcd_main_funcs import *
from vqcd_secondary_funcs import *

def lowest_error_channel(qdim, rank, layers, ansatz, any_chan):
    """
    
    """

    n = 2*qdim
    l = layers # number of layers used for optimization
    an = ansatz # ['1', '2', '3', '4', '5', '6']

    chan_list = np.load(f'data/rand_chan_{qdim}_qubits_{rank}_rank.npy') # load the list of channels
    kraus_chan = Kraus(Stinespring(chan_list[0])) # convert the selected channel to the Kraus form

    _, jcdm = purity_before_diag(qdim, kraus_chan)

    sqrt_jcdm = la.sqrtm(jcdm)       
    fin_opt_ang = np.load(f'data/opt_ang_test/dim{qdim}_opt_ang_rank{rank}_ansatz{an}_layer{l}_final.npy')
    opt_ang = fin_opt_ang.reshape(-1, 2*n)

    dict_chan = {}

    for any_chan_no in range(1, any_chan):
        
        any_kraus_chan = Kraus(Stinespring(chan_list[any_chan_no]))
        _, any_state = purity_before_diag(qdim, any_kraus_chan)

        t1 = np.matmul(sqrt_jcdm, any_state)
        t2 = np.matmul(t1, sqrt_jcdm)
        true_fidelity = np.trace(la.sqrtm(t2)).real
        error = 1    
        TFB, _, _ = trun_output(n, any_state, kraus_chan, opt_ang, an, error, 'sim', 'simulator', 0)
        vtfb = np.abs(TFB - true_fidelity)
        print(vtfb, any_chan_no)
        dict_chan[f'{vtfb}'] = any_chan_no

    dum = []
    for key in dict_chan.keys():
        dum.append(key)
    
    np.save(f'data/fid_plot_test/lowest_error_chan_qdim{qdim}_rank{rank}', dict_chan[f'{min(dum)}'])
    return dict_chan[f'{min(dum)}']

if __name__ == "__main__":
    qdim  = 1
    rank = 4
    layers = 3
    ansatz = 3
    any_chan = 1000
    x = lowest_error_channel(qdim, rank, layers, ansatz, any_chan)
    print(x)