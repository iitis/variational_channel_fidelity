from math import inf

from numpy.ma.core import outerproduct
from scipy.optimize import minimize
from qiskit_ionq import IonQProvider
import scipy.linalg as la
import matplotlib.pyplot as plt
import numpy as np
import random
import sys

from noise_model import *

# qiskit imports
from qiskit import *
from qiskit.providers.aer.extensions.snapshot_statevector import *
from qiskit.aqua.utils import tensorproduct
from qiskit.providers.aer import AerSimulator
from qiskit.quantum_info import DensityMatrix, partial_trace, Kraus, state_fidelity
from qiskit.quantum_info.operators.channel.stinespring import Stinespring
from scipy.optimize import minimize
from ansatz_list import *