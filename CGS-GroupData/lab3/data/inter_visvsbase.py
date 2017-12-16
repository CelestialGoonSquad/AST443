#Jasmine Garani, Lorena Mezini, Patrick Payne
#Created 11/26/17

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

name = 'bsnvs_new.txt'
baseline = np.genfromtxt(name,skip_header=1,usecols = 0)
baseerr = np.genfromtxt(name,skip_header=1,usecols = 1)
vis = np.genfromtxt(name,skip_header=1,usecols = 2)
error = np.genfromtxt(name,skip_header=1,usecols = 3)

plt.plot(baseline,vis, linestyle='none',marker='o')
plt.errorbar(baseline,vis,xerr=baseerr,yerr=error,linestyle='')
plt.xlabel(r'$B_{\lambda}$',fontsize=16)
plt.ylabel(r'Visibility',fontsize=16)


z=np.linspace(0,200,100)
w=abs(np.sin(np.pi*z*0.0082874)/(np.pi*z*0.0082874))
y=abs(np.sin(np.pi*z*0.0093073)/(np.pi*z*0.0093073))
plt.plot(z,w,linestyle="--", label='Fitted Sinc Function')
plt.plot(z,y,linestyle="-",label='Expected Sinc Function')

#plt.show()
#sinc = sin(piBalpha)/piB)

#define the sinc function
def sinc_func(x,a):
    return np.sin(np.pi*x*a)/(np.pi*x*a)


popt, pcov = curve_fit(sinc_func,baseline,vis,0.0093073)
perr = np.sqrt(pcov)
print popt
print pcov
print perr

#plt.plot(baseline, abs(sinc_func(baseline,*popt)), linestyle = '--',label='Fitted Sinc Function')
plt.legend(loc=1)
plt.savefig('sinc-fit.pdf',format='pdf')
plt.show() 
