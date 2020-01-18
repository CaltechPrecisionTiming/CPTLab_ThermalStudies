import numpy as np

# N_resistors = 15
# R0 = 100.0 # Ohms

def V2power(V, R0=100.0, N_resistors=15, N_dut=16):
    R_tot = float(R0*N_resistors)
    power = np.square(V)/R_tot
    I = V/R_tot
    return power/N_dut, I

def power2V(P, R0=100.0, N_resistors=15, N_dut=16):
    P_tot = float(P*N_dut)
    R_tot = R0*N_resistors
    V = np.sqrt(R_tot*P_tot)
    I = V/R_tot
    return V,I
