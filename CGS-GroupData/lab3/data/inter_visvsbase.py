#Jasmine Garani, Lorena Mezini, Patrick Payne
#Created 11/26/17

import numpy as np
import matplotlib.pyplot as plt

name = 'bsnsv.txt'
baseline = np.genfromtxt(name,usecols = 0)
vis = np.genfromtxt(name,usecols = 1)

plt.plot(baseline,vis, linestyle='none',marker='o')
plt.xlabel(r'Baseline (cm)')
plt.ylabel(r'Visibility')
plt.show()
