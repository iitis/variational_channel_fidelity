from extensions import *
from VQCD_secondary_funcs import *

## The cost function evaluator function as given in Fig. 1a & 1b of: https://www.nature.com/articles/s41534-019-0167-6
def cost_func(qdim, theta, kraus_chan, ansatz_no, shots, purity_before_diag):
    """ Calculate the value of the cost function for particular choice of the
    input:
    ------
    qdim = dimention of quantum channel,
    theta = random initial angles,
    channel = kraus operator of the channel,
    ansatz_no = ansatz number,
    shots = number of shors for simulator,
    purity_before_diag = purity of channel before diagonalization,

    return:
    -------
    cost function value

    layered ansatz and the angle. """

    # number of qubits in the full circuit
    n = 2 * qdim

    # n is also the number of parameters in the ansatz
    theta = theta.reshape(-1, 2*n)

    # start the ciruit
    qc_cost = QuantumCircuit(2 * n, 2*qdim)

    # add the selected ansatz twice
    qc_cost = qc_cost.compose(jamilchoi(qdim, kraus_chan), list(range(n)))
    qc_cost = qc_cost.compose(jamilchoi(qdim, kraus_chan), list(range(n, 2 * n)))
    
    if qdim == 1:
        qc_cost = qc_cost.compose(ansatz_2q(n, theta, ansatz_no), list(range(n)))
        qc_cost = qc_cost.compose(ansatz_2q(n, theta, ansatz_no), list(range(n, 2 * n)))
    elif qdim == 2:
        qc_cost = qc_cost.compose(ansatz_4q(n, theta, ansatz_no), list(range(n)))
        qc_cost = qc_cost.compose(ansatz_4q(n, theta, ansatz_no), list(range(n, 2 * n)))

    # add cx operations
    for i in range(n):
        qc_cost.cx([i + n], [i])
    
    # evolve in input matrix
    qc_cost.measure(list(range(2*qdim)), list(range(2*qdim)))
    device = Aer.get_backend('qasm_simulator')
    result = execute(qc_cost, backend = device, shots = shots).result()
    counts = result.get_counts(qc_cost)
    purity_after_diag = counts['0'*2*qdim]/shots
    cost = purity_before_diag - purity_after_diag

    return cost.real


## Returning the estimated eigenvalues as shown in Fig.1c of: https://www.nature.com/articles/s41534-019-0167-6
def eig_info(qdim, theta, kraus_chan, ansatz_no, error, device_type, noise_mdl, noise_amp):
    """
    Return the measurement basis based on the relative error on calculating eigenvalues.
    input:
    ------
        qdim = channel dimension.
        theta = optimized angles obtained corresponding to optimal cost.
        kraus_chan = kraus operators of the channel.
        ansatz_no = the no. of ansatz under use.
        error = threshold for relative error.
        device_type = for simulated -->> 'sim,
                    for real -->> 'real.
        noise_mdl = 
        ***for 'sim'***, specify noise model,
        amplitude damping -->> 'amp_damp',
        depolarizing -->> 'depol',
        random X -->> 'rand_x';
        ***for 'real'***, specify ibmq device,
        e.g. 'ibmq-belem', 'ibmq-lima' etc.
        noise_amp == amplitude of noise, 0 <= noise_amp <= 1.
    #######################
    output:
    -------
        a list containing inferred eigenvalues
    """
    n = 2*qdim
    qc_meas = QuantumCircuit(n)
    qc_meas = qc_meas.compose(jamilchoi(qdim, kraus_chan), list(range(n)))
    
    if qdim ==1:
        qc_meas = qc_meas.compose(ansatz_2q(n, theta, ansatz_no), list(range(n)))
    elif qdim ==2:
        qc_meas = qc_meas.compose(ansatz_4q(n, theta, ansatz_no), list(range(n)))
    for q in range(n//2):
        qc_meas.swap(q, n-q-1)
    
    qc_meas.measure_all()
    shots = 20000
    if device_type == 'sim':

        device = Aer.get_backend('qasm_simulator')
        if noise_mdl == 'amp_damp':
            result = execute(qc_meas, backend = device, noise_model = create_noise_model_amp_damping(noise_amp),
                            shots = shots).result()
        elif noise_mdl == 'depol':
            result = execute(qc_meas, backend = device, noise_model = create_noise_model_depolarazing(noise_amp),
                            shots = shots).result()
        elif noise_mdl == 'rand_x':
            result = execute(qc_meas, backend = device, noise_model = create_noise_model_random_x(noise_amp),
                            shots = shots).result()
        elif noise_mdl == 'simulator':
            result = execute(qc_meas, backend = device, shots = shots).result()

    
    elif device_type == 'real':
        shots = 2000
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub = 'ibm-q')
        print('-----')
        print(noise_mdl)
        print('-----')
        device = provider.get_backend(noise_mdl)
        sim_real = AerSimulator.from_backend(device)
        result = sim_real.run(qc_meas).result()
    
    counts = result.get_counts(qc_meas)
    tmp_counts = {}

    for num in range(0,2**n):
        tmp_counts[format(num,'0{}b'.format(n))] = 0
    for ks in counts.keys():
        tmp_counts[ks] = counts[ks]

    sim_eigval = {}
    for num in range(0,2**n):

        stat_count = tmp_counts[format(num,'0{}b'.format(n))]
        rel_error = np.sqrt(shots)/stat_count

        if rel_error <=  error:
            est_eig = stat_count/shots
            sim_eigval[format(num,'0{}b'.format(n))] = est_eig
        else:
            sim_eigval[f'n{num}'] = 0
    return sim_eigval

## Truncated Fidelity estimator function as described in Fig.1 of: https://arxiv.org/abs/1906.09253 
def trun_output(n, any_state, channel, theta, ansatz_no, error, device_type, noise_mdl, noise_amp):
    """
    Return the measurement basis based on the relative error on calculating eigenvalues.
    input:
    ------
        qdim = channel dimention.
        theta = optimized angles obtained corresponding to optimal cost.
        kraus_chan = kraus operators of the channel.
        ansatz_no = the no. of ansatz under use..
        error = threshold for relative error.
        device_type = for simulated -->> 'sim,
                    for real -->> 'real.
        noise_mdl = for 'sim', specify noise model, amplitude damping -->> 'amp_damp', depolarizing -->> 'depol',
        random X -->> 'rand_x'.
        noise_amp = amplitude of noise, 0<= noise_amp<= 1.
    #######################
    output:
    -------
        truncated fidelity counds i.e. TFB, TGFB values
    """

    eig_dict = eig_info(n//2, theta, channel, ansatz_no, error, device_type, noise_mdl, noise_amp)
    basis = []
    eigval = []

    for key in eig_dict.keys():
        basis.append(key)
        eigval.append(eig_dict[key])
    
    eigenvector = []
    for i in basis:
        if i == 'n':
            eigenvector.append(np.zeros(2 ** n))
        else:
            qc_reg = QuantumRegister(n)
            qc = QuantumCircuit(qc_reg)
            for q in range(len(i)):
                
                if i[q] == '0':
                    qc.id([q])
                else:
                    qc.x([q])
            
            if n//2 == 1:
                qc = qc.compose(ansatz_2q(n, theta, ansatz_no).inverse())
            if n//2 == 2:
                qc = qc.compose(ansatz_4q(n, theta, ansatz_no).inverse())
            
            simulator = Aer.get_backend('statevector_simulator')
            result = execute(qc, simulator).result()
            eigen_vec = result.get_statevector(qc)       
            
            eigenvector.append(eigen_vec)

    T = np.zeros((2**n, 2**n))
    Tlist = []
    
    for r_i in range(len(eigval)):
        for r_j in range(len(eigval)):
            
            outprod = outerproduct(eigenvector[r_i], eigenvector[r_j])
            expval = np.sum(np.diag(np.matmul(any_state, outprod)))
            sqrt_eig = np.sqrt(eigval[r_i] * eigval[r_j])
            Tij = np.multiply(sqrt_eig, expval)
            Tlist.append(Tij)
            T = np.add(T, np.multiply(Tij, outprod))

    sigma = np.asarray(Tlist).reshape(-1,2**n)
    T = np.asmatrix(T)
    eigT = la.eig(T)[0].real

    flag = 0
    for e in eigT:
        if e < 0:
            flag += 1
    
    if flag != 0:
        eigT, _ = maximum_likelihood(T)
    #TFB calculation
    TFB = np.sum(np.sqrt(np.abs(eigT)))
    #TGFB calculation
    if error == 1 :
        TGFB = TFB
    else:
        TGFB = TFB + np.sqrt((1 - sum(eigval))*(1 - sum(np.diag(sigma))))
    
    #counts rank corresponding to threshold of relative error
    m = 0
    for e in eigval:
        if e != 0:
            m +=1
    
    return np.abs(TFB), np.abs(TGFB), m