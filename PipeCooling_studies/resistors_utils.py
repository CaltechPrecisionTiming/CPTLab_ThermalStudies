import numpy as np

N_resistors = 15
R0 = 100.0 # Ohms

def V2power(V):
    R_tot = R0*N_resistors
    power = np.square(V)/R_tot
    I = V/R_tot
    return power/16.0, I

def power2V(P):
    P_tot = float(P)*16
    R_tot = R0*N_resistors
    V = np.sqrt(R_tot*P_tot)
    I = V/R_tot
    return V,I
