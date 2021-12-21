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

        opt_ang = optimal angle.

        an = ansatz no. under consideration

        device_type = for simulated -->> 'sim',
                    for real -->> 'real'.
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
                
                _, tgfb, m = trun_output(n, any_state, kraus_chan, opt_ang, an, error, device_type, noise_mdl, noise_amp)
                if m == x and tgfb <= 1:
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
layers = 3 # number of layers used for optimization
times = 1 # number of runs for each layer
an = 3 # optimize using selected anasatze

device_type = 'sim'

if device_type == 'sim':
    noise_mdl_list = ['amp_damp', 'depol']#, 'rand_x']#, 'simulator']
    noise_amp_list = [0, 0.05, 0.1, 0.5, 1]
elif device_type == 'real':
    noise_mdl_list = ['ibmq_manila', 'ibmq_lima']
    noise_amp_list = [0]

chan_list = np.load(f'chan_data/rand_chan_{qdim}_qubits_{rank}_rank.npy') # load the list of channels
kraus_chan = Kraus(Stinespring(chan_list[chan_no])) # convert the selected channel to the Kraus form
purity_before_diag_val, jcdm = purity_before_diag(qdim, kraus_chan)
sqrt_jcdm = la.sqrtm(jcdm)
true_eig = la.eig(jcdm)[0] # true fidelity
any_chan_no = np.load(f'chan_data/fid_plot_test/lowest_error_chan_qdim{qdim}_rank{rank}/.npy')
shots = 20000

for noise_mdl in noise_mdl_list:
    for noise_amp in noise_amp_list:
        
        print('---------')
        print(f'noise model {noise_mdl}')
        print(f'noise model {noise_amp}')
        print('---------')
        fin_opt_ang = np.load(f'chan_data/opt_ang_test/dim{qdim}_opt_ang_rank{rank}_ansatz{an}_layer{layers}_final.npy')
        
        if device_type == 'real' or device_type == 'sim' and noise_mdl == 'simulator':
            layers_list = list(range(1, layers+1))
        elif device_type == 'sim':
            layers_list = list(range(layers, layers+1))
        
        for l in layers_list:

            opt_ang = fin_opt_ang.reshape(-1, 2*n)
            opt_ang = opt_ang[0:l]
            sum_fid_tfb = 0
            sum_fid_tgfb = 0
            sum_fid_tfb_less_than_five_percent = 0
            sum_fid_tgfb_less_than_five_percent = 0
            any_kraus_chan = Kraus(Stinespring(chan_list[any_chan_no]))
            _, any_state = purity_before_diag(qdim, any_kraus_chan)
            t1 = np.matmul(sqrt_jcdm, any_state)
            t2 = np.matmul(t1, sqrt_jcdm)
            true_fidelity = np.trace(la.sqrtm(t2)).real
            
            np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_true_fid_rank{rank}_ansatz{an}', true_fidelity)
            if len(layers_list) > 1:
                error_list, m_list = [1], [rank] #error_val_list(qdim, rank, any_chan_no, kraus_chan, opt_ang, shots, an, device_type, noise_mdl, noise_amp)
            else:
                error_list, m_list = error_val_list(qdim, rank, any_chan_no, kraus_chan, opt_ang, an, device_type, noise_mdl, noise_amp)
            
            np.save(f'chan_data/fid_plot_data_test/qdim{qdim}_rank{rank}_error_list_{noise_mdl}_{noise_amp}', error_list)
            np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_m_list_rank{rank}_ansatz{an}_{noise_mdl}_{noise_amp}', m_list)
            for error in error_list:                                
               
                TFB, TGFB, m = trun_output(n, any_state, kraus_chan, opt_ang, an, error, device_type, noise_mdl, noise_amp)
                print(TFB, TGFB, m)
                vtfb = np.abs(TFB)
                vtgfb = np.abs(TGFB)
                
                print('trun fidelity bound')
                print(vtgfb, vtfb)
                print('----')
                print('true fidelity')
                print(true_fidelity)
                print('----')
                
                np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_lower_bound_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}_{device_type}{noise_mdl}_{noise_amp}_layers{l}', vtfb)
                np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_upper_bound_rel_error{error}_rank{rank}_ansatz{an}_anychan{any_chan_no}_{device_type}{noise_mdl}_{noise_amp}_layers{l}', vtgfb)
                # else:
                #     np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_lower_bound_rel_error{int(error)}_rank{rank}_ansatz{an}_anychan{any_chan_no}_{device_type}{noise_mdl}_{noise_amp}_layers{l}', vtfb)
                #     np.save(f'chan_data/fid_plot_data_test/qbit{qdim}_upper_bound_rel_error{int(error)}_rank{rank}_ansatz{an}_anychan{any_chan_no}_{device_type}{noise_mdl}_{noise_amp}_layers{l}', vtgfb)