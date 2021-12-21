from qiskit import QuantumCircuit

# TODO: include description and rationale for using each of the ansatzes

def ansatz_4q(n,theta, ansatz_no):
    circ = QuantumCircuit(n)
    if ansatz_no == 1:
        for t in theta:
            circ.ry(t[0], [0])
            circ.rz(t[1], [0])
            circ.ry(t[2], [0])
            circ.ry(t[3], [1])
            circ.rz(t[4], [1])
            circ.ry(t[5], [1])
            circ.ry(t[6], [2])
            circ.rz(t[7], [2])
            circ.ry(t[0], [2])
            circ.ry(t[1], [3])
            circ.rz(t[2], [3])
            circ.ry(t[3], [3])
            
            circ.cx([0],[1])
            circ.cx([1],[2])
            circ.cx([2],[3])
            circ.cx([3],[0])
    
    if ansatz_no == 2:
        for t in theta:
            circ.rz(t[0], [0])
            circ.rz(t[1], [1])
            circ.rz(t[2], [2])
            circ.rz(t[3], [3])
            circ.rx(t[4], [0])
            circ.rx(t[5], [1])
            circ.rx(t[6], [2])
            circ.rx(t[7], [3])

            circ.cz([0],[1])
            circ.cz([1],[2])
            circ.cz([2],[3])
            circ.cz([3],[0])

    if ansatz_no == 3:
        for t in theta:
            circ.ry(t[0], [0])
            circ.ry(t[1], [1])
            circ.ry(t[2], [2])
            circ.ry(t[3], [3])
            circ.rz(t[4], [0])
            circ.rz(t[5], [1])
            circ.rz(t[6], [2])
            circ.rz(t[7], [3])

            circ.cx([0],[1])
            circ.cx([1],[2])
            circ.cx([2],[3])
            circ.cx([3],[0])

    if ansatz_no == 4:
        for t in theta:
            circ.ry(t[0], [0])
            circ.ry(t[1], [1])
            circ.ry(t[2], [2])
            circ.ry(t[3], [3])
            circ.ry(t[4], [0])
            circ.ry(t[5], [1])
            circ.ry(t[6], [2])
            circ.ry(t[7], [3])

            circ.cx([0],[1])
            circ.cx([1],[2])
            circ.cx([2],[3])
            circ.cx([3],[0])

            circ.ry(t[0], [0])
            circ.ry(t[1], [1])
            circ.ry(t[2], [2])
            circ.ry(t[3], [3])
            circ.ry(t[4], [0])
            circ.ry(t[5], [1])
            circ.ry(t[6], [2])
            circ.ry(t[7], [3])

    return circ

def ansatz_2q(n, theta, ansatz_no):
    """"
    Return one of the the considered 2-qubit anasatzes as a quantum circuit with fixed angels.
    """

    circ = QuantumCircuit(n)
    if ansatz_no == 1:
        for t in theta:
            circ.rz(t[0], [0])
            circ.ry(t[1], [0])
            circ.rz(t[2], [1])
            circ.ry(t[3], [1])
            circ.cx([0], [1])
    elif ansatz_no == 2:
        for t in theta:
            circ.rx(t[0], [0])
            circ.rz(t[1], [0])
            circ.rx(t[2], [1])
            circ.rz(t[3], [1])
            circ.cx([0], [1])
    elif ansatz_no == 3:
        for t in theta:
            circ.rz(t[0], [0])
            circ.ry(t[1], [0])
            circ.rz(t[2], [1])
            circ.ry(t[3], [1])
            circ.cz([0], [1])
    elif ansatz_no == 4:
        for t in theta:
            circ.rx(t[0], [0])
            circ.rz(t[1], [0])
            circ.rx(t[2], [1])
            circ.rz(t[3], [1])
            circ.cz([0], [1])
    elif ansatz_no == 5:
        for t in theta:
            circ.ry(t[0], [0])
            circ.rz(t[1], [0])
            circ.ry(t[2], [0])
            circ.ry(t[3], [1])
            circ.rz(t[0], [1])
            circ.ry(t[1], [1])
            circ.cz([0], [1])
    elif ansatz_no == 6:
        for t in theta:
            circ.ry(t[0], [0])
            circ.rz(t[1], [0])
            circ.ry(t[2], [0])
            circ.ry(t[3], [1])
            circ.rz(t[0], [1])
            circ.ry(t[1], [1])
            circ.cx([0], [1])
    return circ
