import numpy as np
import matplotlib.pyplot as plt

f_time = np.genfromtxt("Base-Inter-55-05.txt",skip_header=7,usecols = 0)
f_pot = np.genfromtxt("Base-Inter-55-05.txt",skip_header=7,usecols = 1)

def gaussian(t,sigma):
    """ a gaussian kernel """

    g = 1.0/(sigma*np.sqrt(2.0*np.pi))*np.exp(-0.5*(t/sigma)**2)
    g = g[:] + g[::-1]
    gsum = np.sum(g)
    return g/gsum

def do_convolve(t,sig,kernal):
    fft_kernal = np.fft.rfft(kernal)
    fft_sig = np.fft.rfft(sig)
    
    conv = fft_sig*fft_kernal
    f_conv = np.fft.irfft(conv)

    return f_conv

sigmas = [0.01,0.03,0.05,0.075,0.10]
i = [0.2,0.4,0.6,0.8,1.0]
for s in range(len(sigmas)):
    smooth_pot = do_convolve(f_time,f_pot,gaussian(f_time,sigmas[s]))
    smooth_pot = smooth_pot + i[s]
    plt.plot(f_time,smooth_pot,label = str(sigmas[s]))

plt.plot(f_time,f_pot,label = "true")
plt.legend()
plt.savefig("guassian_smoothed_inter_obsv.png")
plt.show()
