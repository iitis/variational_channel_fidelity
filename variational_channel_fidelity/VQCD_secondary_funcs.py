from extensions import *

# converts a quantum channel into an equivalent CPTP quantum state as given in: https://link.springer.com/article/10.1007/s11128-010-0166-1 
def jamilchoi(qdim, kraus_chan):
    """
    Returns quantum circuit corresponding to the channel-state duality.
    """
    qr_jamil = QuantumRegister(2 * qdim)
    qc_jamil = QuantumCircuit(qr_jamil)
    qc_jamil.h([0])
    
    for q in range(2*qdim - 1):
        qc_jamil.cx([q], [q + 1])
    for q in range(qdim):
        qc_jamil.id(q)
    
    k = [sum(x) for x in zip(list(range(qdim)), [qdim] * qdim)]
    qc_jamil.append(kraus_chan, k)
    return qc_jamil


## returns the purity of a random quantum channel 
def purity_before_diag(qdim, kraus_chan):
    """
    Returns purity and the density matrix before diagonalization.
    """
    qc_trace = QuantumCircuit(2*qdim)
    qc_trace = qc_trace.compose(jamilchoi(qdim, kraus_chan), list(range(2*qdim)))
    dm_jamilchoi  = DensityMatrix.from_label('0'*2*qdim).evolve(qc_trace)
    dm = dm_jamilchoi.data
    before = np.trace(np.matmul(dm,dm))
    return before.real, dm

# maximal likelihood of a trace <= 1 matrix:
def maximum_likelihood(T):
    """
    returns eigenvalues and matrix after maximal likelihood
    input:
    ------
    T = matrix with negative eigenvalues.
    """
    norm = np.trace(T)
    T = T/norm
    eig_values, eig_vectors = la.eig(T)
    idx = eig_values.argsort()[::-1]   
    sorted_eigval = eig_values[idx]
    sorted_eigvec = eig_vectors[:,idx]
    transposed_sorted_eigvec= sorted_eigvec.T
    no_of_eig = len(sorted_eigval)
    i = len(sorted_eigval)
    a = 0
    lamda = []
    for eig_no in range(len(sorted_eigval)):

        mu = sorted_eigval[no_of_eig - eig_no - 1].real
        x = mu + (a/i)
        if x < 0:
            lamda.append(0)
            a += sorted_eigval[i-1].real
            i-=1
        else:
            lamda.append(x)

    #
    lamda = np.multiply(list(reversed(lamda)), np.abs(norm))
    outer = outerproduct(transposed_sorted_eigvec[0],transposed_sorted_eigvec[0])
    mat = np.multiply(lamda[0], outer)
    for el in range(1, len(lamda)):

        outer = outerproduct(transposed_sorted_eigvec[el],transposed_sorted_eigvec[el])
        mat += np.multiply(lamda[el], outer)
    return lamda, np.asmatrix(mat)