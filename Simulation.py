#The simulation:

 #Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from qutip import *
import pandas as pd
import csv
from datetime import datetime
import scipy
from scipy.linalg import svdvals
from scipy.special import comb

#Eigenstates of the system's Hamiltonian based on the Fig.2 of this paper

#0_logic
psi1 = (0.776144941 * basis(16, 1) + 0.612190015 * basis(16, 5) + 0.288521700 * basis(16, 9) + 0.111845332 * basis(16, 13)). unit()
#1_logic
psi2 = (0.904229459 * basis(16, 3) + 0.423327595 * basis(16, 7)+ 0.143263497  * basis(16, 11) + 0.103585320 * basis(16, 15)).unit()

#initial states (density matrices) for tracking the bit flip error behaviour
rho_sys1 = ket2dm(psi1)
rho_sys2 = ket2dm(psi2)

#initial states (density matrices) of the ancillary qubit
rho_anc = ket2dm(basis(2, 0))

#initial coupled density matrices
rho_initial1 = tensor(rho_sys1 , rho_anc)
rho_initial2 = tensor(rho_sys2 , rho_anc)

#Target density matrices (traced out on ancillary qubit)
rho_target1 = tensor(rho_sys1, qeye(2))
rho_target2 = tensor(rho_sys2, qeye(2))



#Parameters
hbar = 1
K = 40 * np.pi
DeltaKPO = 60 * np.pi
DeltaAnc = 2100 * np.pi
P = 11.081 * np.pi
g = 14 * np.pi
Acor = 0.5 * np.pi
wcor = 2100.72 * np.pi
gammaKPO = 0.02
gammaANC = 1.114 * np.pi
n = 0.00001
t = 100

#Ladder coupled Operators
a = tensor(destroy(16), qeye(2))
b = tensor(qeye(16), destroy(2))


#Compound system and ancillary Hamiltonian

#Time-dependent part of the Hamiltonian
def coeff(t):
    return 0.5 * np.pi * np.cos(2100.72 * np.pi * (t))

#Time-independent part of the Hamiltonian
H5 = (a.dag() @ b.dag() + a @ b)
Hd = DeltaKPO * a.dag() @ a
Hk = (K / 2) * a.dag() @ a.dag() @ a @ a
Hp = (P / 2) * (a.dag() @ a.dag() @ a.dag() @ a.dag() + a @ a @ a @ a)
Ha = DeltaAnc * b.dag() @ b
Hg = g * (a.dag() @  b + a @ b.dag())
H0 = hbar * (Hd - Hk + Hp + Ha + Hg)

#Total time-dependent Hamiltonian
H = [H0, [H5, coeff]]

#collapse operators
c_ops = [np.sqrt((n + 1) * gammaKPO) * a, np.sqrt(gammaANC) * b]

#Tracking run-time of the code
start = datetime.now()

#Time-evolution

#setting time-steps
dt = 0.3 / max(K, DeltaKPO, DeltaAnc, P, g, Acor, wcor, gammaKPO, gammaANC)
times = np.linspace(0, 100, 1000)

#Setting the Mesolve function of Qutip
options = Options(nsteps=1000000000)
result1 = mesolve(H, rho_initial1, times, c_ops, options=options)
result2 = mesolve(H, rho_initial2, times, c_ops, options=options)




# Calculate populations
P_0_0 = [fidelity(rho_target1, state) for state in result1.states]
P_1_0 = [fidelity(rho_target2, state) for state in result1.states]

P_1_1 = [fidelity(rho_target2, state) for state in result2.states]
P_0_1 = [fidelity(rho_target1, state) for state in result2.states]

#Retrieving the Upper and Lower bounds of the plot associated with the bit-flip error
Pu = [(P0 + P1) / 2 for P0, P1 in zip(P_0_0, P_1_1)]
Pd = [(P0 + P1) / 2 for P0, P1 in zip(P_1_0, P_0_1)]



# Plot results
plt.plot(times, Pu, color="pink")
plt.plot(times, Pd, color="red")
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend()
plt.title("Population Dynamics with AQEC")
plt.show()

end = datetime.now()
td = ((end - start) / 60).total_seconds()
print(f"The time of execution of above program is : {td:.03f}s")
