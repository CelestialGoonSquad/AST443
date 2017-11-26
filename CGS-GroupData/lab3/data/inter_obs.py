import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

name = "Base-Inter-55-05.txt"
f_time = np.genfromtxt(name,skip_header=7,usecols = 0)
f_pot = np.genfromtxt(name,skip_header=7,usecols = 1)


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
    if "50-07" in name:
        smooth_pot = do_convolve(f_time[:-1],f_pot[:-1],gaussian(f_time[:-1],sigmas[s]))
        smooth_pot = smooth_pot + i[s]
        plt.plot(f_time[:-1],smooth_pot,label = str(sigmas[s]))
        maxInd = argrelextrema(smooth_pot, np.less)
        minInd = argrelextrema(smooth_pot, np.greater)
        m = smooth_pot[minInd]
        r = smooth_pot[maxInd]
        tr = f_time[maxInd]
        tm = f_time[minInd]
        for j in range(len(r)):
            print "time,max vals = ",tr[j],r[j]
        for j in range(len(m)):
            print "time,min vals = ",tm[j],m[j]
    else:
        smooth_pot = do_convolve(f_time,f_pot,gaussian(f_time,sigmas[s]))
        smooth_pot = smooth_pot + i[s]
        plt.plot(f_time,smooth_pot,label = str(sigmas[s]))
        maxInd = argrelextrema(smooth_pot, np.less)
        minInd = argrelextrema(smooth_pot, np.greater)
        m = smooth_pot[minInd]
        r = smooth_pot[maxInd]
        tr = f_time[maxInd]
        tm = f_time[minInd]
        for j in range(len(r)):
            print "time,max vals = ",tr[j],r[j]
        for j in range(len(m)):
            print "time,min vals = ",tm[j],m[j]

print "For True Vals"
maxInd = argrelextrema(f_pot, np.less)
minInd = argrelextrema(f_pot, np.greater)
r = f_pot[maxInd]
m = f_pot[minInd] 
tr = f_time[maxInd]
tm = f_time[minInd]
for j in range(len(r)):
    print "time,max vals = ",tr[j],r[j]
for j in range(len(m)):
    print "time,min vals = ",tm[j],m[j]

plt.plot(f_time,f_pot,label = "true")
plt.title("35-11")
plt.legend()
#plt.savefig("gaussian_smoothed_inter_obsv_30-12.png")
plt.show()
