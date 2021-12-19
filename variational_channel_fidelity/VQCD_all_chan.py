from VQCD_main_funcs import *
from VQCD_secondary_funcs import *


# returns the list of required relative error for which we get a different ranks
def error_val_list(qdim, rank, any_chan_no, kraus_chan, opt_ang, an, device_type, noise_mdl, noise_amp):
    """  
    returns a list containing threshold of relative error for different rank
    input:
    ------
        qdim = channel dimension.
        rank = rank of the matrix.
        any_chan_no = the reference channel. any_chan_no >= 1
        kraus_chan = kraus operators of the channel.
        opt_ang = optimal angle,
        an = ansatz no. under consideration
        device_type = for simulated -->> 'sim,
                    for real -->> 'real.
        noise_mdl = for 'sim', specify noise model, amplitude damping -->> 'amp_damp', depolarizing -->> 'depol',
        random X -->> 'rand_x'.
        noise_amp = amplitude of noise, 0<= noise_amp<=1.
    ###############
    output:
    -------
        a list containing threshold of relative error for different rank
    """
    chan_list = np.load(f'chan_data/rand_chan_{qdim}_qubits_{rank}_rank.npy')
    any_kraus_chan = Kraus(Stinespring(chan_list[any_chan_no]))
    _, any_state = purity_before_diag(qdim, any_kraus_chan)
    n = 2*qdim
    error_list = []
    m_list = []
    s = 0.001
    error = 0.018
    for x in range(1, rank+1):
        if x < rank:
            for error in np.arange(0+error, 1.01, s):
                
                _, _, m = trun_output(n, any_state, kraus_chan, opt_ang, an, error, device_type, noise_mdl, noise_amp)
                if m == x:
                    error_list.append(error)
                    m_list.append(m)
                    break
                else:
                    continue
        else:
            error_list.append(1.0)
            m_list.append(rank)
        s += 0.0005
        continue

    return error_list, m_list


if len(sys.argv) < 2:
    chan_no = 0
else:
    chan_no = int(sys.argv[1])

qdim = 1 # number of qubits for the channel
n = 2*qdim
rank = 4 # rank of the channel (1<rank<2^qdim)
l = 3 # number of layers used for optimization
times = 1 # number of runs for each layer
an = 3 # ['1', '2', '3', '4', '5', '6']

optimize_methods = ['Powell', 'COBYLA', 'L-BFGS-B'] # possible methods

chan_list = np.load(f'chan_data/rand_chan_{qdim}_qubits_{rank}_rank.npy') # load the list of channels
kraus_chan = Kraus(Stinespring(chan_list[chan_no])) # convert the selected channel to the Kraus form

purity_before_diag_val, jcdm = purity_before_diag(qdim, kraus_chan)

sqrt_jcdm = la.sqrtm(jcdm)
true_eig = la.eig(jcdm)[0] # true fidelity
any_chan = 1000
shots = 20000


fin_opt_ang = np.load(f'chan_data/opt_ang_test/dim{qdim}_opt_ang_rank{rank}_ansatz{an}_layer{l}_final.npy')
opt_ang = fin_opt_ang.reshape(-1, 2*n)

for any_chan_no in range(1, any_chan):

    print(f'channel {any_chan_no} done')
    any_kraus_chan = Kraus(Stinespring(chan_list[any_chan_no]))
    _, any_state = purity_before_diag(qdim, any_kraus_chan)

    t1 = np.matmul(sqrt_jcdm, any_state)
    t2 = np.matmul(t1, sqrt_jcdm)
    true_fidelity = np.trace(la.sqrtm(t2)).real
    error_list, m_list = error_val_list(qdim, rank, any_chan_no, kraus_chan, opt_ang, an, 'sim', 'simulator', 0)
    print(error_list)
    print(f'for channel {any_chan_no}, m_list {m_list}')
    
    np.save(f'chan_data/fid_plot_data_test/qdim{qdim}_rank{rank}_error_list_simulator_anychan{any_chan_no}', error_list)
    np.save(f'chan_data/fid_plot_data_test/qdim{qdim}_rank{rank}_m_list_simulator_all_chan', m_list)

    for error in error_list:                               
        TFB, TGFB, _ = trun_output(n, any_state, kraus_chan, opt_ang, an, error, 'sim', 'simulator', 0)

        vtfb = np.abs(TFB - true_fidelity)
        vtgfb = np.abs(TGFB- true_fidelity)

        print(vtfb, vtgfb)
        np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_lower_bound_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}', vtfb)
        np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_upper_bound_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}', vtgfb)
        
        if vtfb < 0.05 and vtgfb < 0.05:
            print(any_chan_no)
            np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_lower_bound_less_than5pe_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}', vtfb)
            np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_upper_bound_less_than5pe_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}', vtgfb)
