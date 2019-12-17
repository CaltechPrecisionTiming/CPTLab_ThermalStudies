import numpy as np
import matplotlib.pyplot as plt

def adc2R(c, R=19e3, Vref=2.5):
    s = Vref/4096
    V = s*c
    rT = V*R/(Vref-V)
    return rT


def R2adc(r, R=19e3, Vref=2.5):
    V = Vref*r/(r+R)
    adc = np.floor(4096*V/Vref)
    return adc


def R2T(R, beta=3892.0, T0=25.0, R0=5e3):
    T0 += 273.15
    r_inf = R0*np.exp(-beta/T0)
    T = beta/np.log(R.astype('float')/r_inf)
    return T - 273.15


def T2R(T, beta=3892.0, T0=25.0, R0=5e3):
    T0 += 273.15
    r_inf = R0*np.exp(-beta/T0)
    T_K = T + 273.15
    return r_inf*np.exp(beta/T_K)


def adc2T(c):
    return R2T(adc2R(c))

def T2adc(T):
    return R2adc(T2R(T))
