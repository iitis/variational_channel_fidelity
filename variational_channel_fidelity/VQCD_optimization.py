from VQCD_main_funcs import *
from VQCD_secondary_funcs import *

if len(sys.argv) < 2:
    chan_no = 0
else:
    chan_no = int(sys.argv[1])

qdim = 1 # number of qubits for the channel
n = 2*qdim
rank = 4 # rank of the channel (1<rank<2^qdim)
layers = 3 # number of layers used for optimization
times = 20 # number of runs for each layer
an = 3 # ['1', '2', '3', '4', '5', '6']

optimize_methods = ['Powell', 'COBYLA', 'L-BFGS-B'] # possible methods

chan_list = np.load(f'chan_data/rand_chan_{qdim}_qubits_{rank}_rank.npy') # load the list of channels
kraus_chan = Kraus(Stinespring(chan_list[chan_no])) # convert the selected channel to the Kraus form

purity_before_diag_val, jcdm = purity_before_diag(qdim, kraus_chan)
error = 1

sqrt_jcdm = la.sqrtm(jcdm)
true_eig = la.eig(jcdm)[0] # true fidelity
any_chan = 10
shots = 20000

def cost(theta):
    return cost_func(qdim, theta, kraus_chan, an, shots, purity_before_diag_val)

opt_ang_dict = {}
for _ in range(times):

    initial_guess = np.random.random(2*n*layers)                        
    res = minimize(cost, initial_guess, method=optimize_methods[1], options={'maxiter': 50})
    initial_guess = res.x
    ang = res.x
    opt_ang = ang.reshape(-1, 2*n)
    tfb = 0
    tgfb = 0
    for any_chan_no in range(1, any_chan):
        
        any_kraus_chan = Kraus(Stinespring(chan_list[any_chan_no]))
        _, any_state = purity_before_diag(qdim, any_kraus_chan)
        t1 = np.matmul(sqrt_jcdm, any_state)
        t2 = np.matmul(t1, sqrt_jcdm)
        true_fidelity = np.trace(la.sqrtm(t2)).real
        TFB, TGFB, _ = trun_output(n, any_state, kraus_chan, opt_ang, an, error, 'sim', 'simulate', 0)
        vtfb = np.abs(TFB - true_fidelity)
        vtgfb = np.abs(TGFB- true_fidelity)
        tfb += vtfb
        tgfb += vtgfb

    tfb /= any_chan_no
    tgfb /= any_chan_no
    opt_ang_dict[f'{tfb}'] = opt_ang
    
    dum = []
    for key in opt_ang_dict.keys():
        dum.append(key)
    print(dum)

fin_opt_ang = opt_ang_dict[f'{min(dum)}']
print(f'the optimal angle has been saved, with error {min(dum)}')
np.save(f'chan_data/opt_ang_test/dim{qdim}_opt_ang_rank{rank}_ansatz{an}_layer{layers}_final', fin_opt_ang)