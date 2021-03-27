import numpy as np
import scipy as sp
    
class sample:
    def __init__(self,filename):
        self.filename = filename
        self.type = self.__computa_tipo_de_sinal()
        self.ts = sp.fromfile(open(filename), dtype = sp.float32)
        self.centered_and_normalized = self.__compute_center_and_normalize()
        #self.standard_deviation = self.__compute_standard_deviation()
        self.inst_freq = self.__compute_inst_freq()
        
        self.gamma_max = self.__compute_gamma_max()
        self.sigma_af = self.__compute_sigma_af()
        self.sigma_aa = self.__compute_sigma_aa()
        self.sigma_dp = self.__compute_sigma_dp()
        self.sigma_ap = self.__compute_sigma_ap()

    ### Eq 5.2
    def __compute_center_and_normalize(self):
        """Centrar e normalizar"""
        mi_A = np.mean(self.ts) # Eq 5.3
        A_c = self.ts - mi_A
        A_cn = A_c / max(np.abs(A_c))
        return A_cn    


    ### Eq 5.1
    def __compute_gamma_max(self):
    
        """Computa \gamma_{max}"""
        A_cn = self.centered_and_normalized 
        power_spectrum = np.abs(np.fft.fft(A_cn)) ** 2
        gamma_max = max(power_spectrum)/len(A_cn)
        return gamma_max


    ### Eq 5.6
    ### def spectrum_symetry(x):
    ###    #lower_power = np.sum((np.fft(x)) ** 2)
    ###    pass

    def __compute_standard_deviation(self, a, threshold = 0):
    #    a_pos = a.clip(min = abs(threshold))
    #    a_neg = a.clip(max = -abs(threshold))
    #    a = a_pos+a_neg ### concatenando as listas acima de +threshold e abaixo de -threshold
        p_1 = np.mean(np.square(a))
        p_2 = (np.mean(a))**2
        sigma = np.sqrt(p_1 - p_2)
        return sigma

    ### Eq 5.11
    def __compute_sigma_af(self):
        return self.__compute_standard_deviation(abs(self.inst_freq))

    ### Eq 5.10
    def __compute_sigma_aa(self):
        return self.__compute_standard_deviation(abs(self.centered_and_normalized))    
        
    def __compute_inst_freq(self):
        z = sp.signal.hilbert(self.ts)
        inst_phase = np.unwrap(np.angle(z))
        return np.diff(inst_phase)/2*np.pi*128000

    ### Eq 5.5 
    def __compute_sigma_dp(self):
        return self.__compute_standard_deviation(sp.signal.wiener(self.ts))

    ### Eq 5.4    
    def __compute_sigma_ap(self):
        return self.__compute_standard_deviation(abs(sp.signal.wiener(self.ts)))
        
    ### Eq 5.18
    def threshold(self, a, b):
        x = (self.__compute_standard_deviation(a)*np.mean(b))
        y = (self.__compute_standard_deviation(b)*np.mean(a))
        z = (self.__compute_standard_deviation(a)+self.__compute_standard_deviation(b))
        return (x+y)/z
        
    def plot(self, data):
        pass
