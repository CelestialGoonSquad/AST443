#Jasmine Garani, Lorena Mezini, Patrick Payne
#Created 11/26/17

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

name = 'bsnsv-again.txt'
baseline = np.genfromtxt(name,usecols = 0)
vis = np.genfromtxt(name,usecols = 1)

plt.plot(baseline,vis, linestyle='none',marker='o')
plt.xlabel(r'Baseline (cm)')
plt.ylabel(r'Visibility')


#sinc = sin(piBalpha)/piB)

#define the sinc function
def sinc_func(b,a):
    return np.sin(np.pi*b*a)/(np.pi*b)


popt, pcov = curve_fit(sinc_func,baseline,vis)
print popt
print pcov

plt.plot(baseline, sinc_func(baseline,*popt), linestyle = '--')
plt.savefig('sinc-fit.pdf',format='pdf')
plt.show()
