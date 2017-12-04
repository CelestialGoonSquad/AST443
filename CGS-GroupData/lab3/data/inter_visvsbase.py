#Jasmine Garani, Lorena Mezini, Patrick Payne
#Created 11/26/17

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

name = 'bsnvs.txt'
baseline = np.genfromtxt(name,skip_header=1,usecols = 0)
vis = np.genfromtxt(name,skip_header=1,usecols = 1)
error = np.genfromtxt(name,skip_header=1,usecols=2)

plt.plot(baseline,vis, linestyle='none',marker='o')
plt.errorbar(baseline,vis,yerr=error,linestyle='')
plt.xlabel(r'Baseline (cm)')
plt.ylabel(r'Visibility')


z=np.linspace(30,75,100)
y=abs(np.sin(np.pi*z*0.0093073)/(np.pi*z*0.0093073))
plt.plot(z,y,linestyle="-")

#plt.show()
#sinc = sin(piBalpha)/piB)

#define the sinc function
def sinc_func(x,a):
    return np.sin(np.pi*x*a)/(np.pi*x*a)


popt, pcov = curve_fit(sinc_func,baseline,vis,0.01)
print popt
print pcov

plt.plot(baseline, sinc_func(baseline,*popt), linestyle = '--')
plt.savefig('sinc-fit.pdf',format='pdf')
plt.show() 
