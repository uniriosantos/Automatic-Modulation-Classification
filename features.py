import numpy as np
from scipy import signal, misc

### Eq 5.2
def center_and_normalize(a):
    """Centrar e normalizar"""
    mi_A = np.mean(a) # Eq 5.3
    A_c = a - mi_A
    A_cn = A_c / max(np.abs(A_c))
    return A_cn

### Eq 5.1
def gamma_max(a):
    A = center_and_normalize(a)
    """Computa \gamma_{max}"""
    A_cn = center_and_normalize(A) 
    power_spectrum = np.abs(np.fft.fft(A_cn)) ** 2
    gamma_max = max(power_spectrum)/len(A)
    return gamma_max


### Eq 5.6
def spectrum_symetry(x):
    #lower_power = np.sum((np.fft(x)) ** 2)
    pass

def standard_deviation(a, threshold = 0):
#    a_pos = a.clip(min = abs(threshold))
#    a_neg = a.clip(max = -abs(threshold))
#    a = a_pos+a_neg ### concatenando as listas acima de +threshold e abaixo de -threshold
    p_1 = np.mean(np.square(a))
    p_2 = (np.mean(a))**2
    sigma = np.sqrt(p_1 - p_2)
    return sigma

### Eq 5.11
def sigma_af(a):
    return standard_deviation(abs(inst_freq(a)))

### Eq 5.10
def sigma_aa(a):
    return standard_deviation(abs(center_and_normalize(a)))    
    
def inst_freq(a):
    z = signal.hilbert(a)
    inst_phase = np.unwrap(np.angle(z))
    return np.diff(inst_phase)/2*np.pi*128000

### Eq 5.5 
def sigma_dp(a):
    return standard_deviation(signal.wiener(a))

### Eq 5.4    
def sigma_ap(a):
    return standard_deviation(abs(signal.wiener(a)))
    
### Eq 5.18
def threshold(a,b):
    x = (standard_deviation(a)*np.mean(b))
    y = (standard_deviation(b)*np.mean(a))
    z = (standard_deviation(a)+standard_deviation(b))
    return (x+y)/z

def tipo_de_sinal(x):
    """Entra com filename, sai o tipo via string"""
    x = x.partition('/')[2]
    return x.partition('/')[0]

