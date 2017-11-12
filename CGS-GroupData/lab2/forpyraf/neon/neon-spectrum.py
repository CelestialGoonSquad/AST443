# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 20:53:25 2017

@author: Jasmine
"""

import numpy as np
import matplotlib.pyplot as plt

with open("/Users/ilovealltigers/SBU_F17/AST_443/LAB1/CGS-GroupData/lab2/forpyraf/neon/all-images.cal.txt") as f:
    lines = f.readlines()
    x = [line.split()[0] for line in lines]
    y = [line.split()[1] for line in lines]

#print x
#print y

#f, (ax1, ax2)= plt.subplots(2, sharex=True, sharey=True)

# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.

plt.figure(1)
ax1 = plt.subplot(211)
plt.plot(x,y)

plt.xlim([6200.0, 7000.0])
plt.tick_params(axis='x', labelsize=0)
plt.ylim([0, 1.0e-10])
plt.tick_params(axis='y', labelsize=10)
plt.ylabel(r'Flux (1e-11)', fontsize=14)
plt.minorticks_on()

ax1.yaxis.get_offset_text().set_visible(False)

plt.yticks( np.arange(0,1.0e-10,3.0e-11))

#NeonLines
plt.axvline(6233.94,linestyle='dotted',color='red') #He II
plt.axvline(6311.95,linestyle='dotted',color='red') #[S III]
plt.axvline(6406.45,linestyle='dotted',color='red') #He II
plt.axvline(6435.11,linestyle='dotted',color='red') #[Ar V]
plt.axvline(6548.03,linestyle='dotted',color='red') #[N II]
plt.axvline(6562.82,linestyle='dotted',color='red') #H I
plt.axvline(6583.41,linestyle='dotted',color='red') #[N II]
plt.axvline(6678.15,linestyle='dotted',color='red') #He I
plt.axvline(6716.47,linestyle='dotted',color='red') #[S II]
plt.axvline(6730.85,linestyle='dotted',color='red') #[S II]
plt.axvline(6780.14,linestyle='dotted',color='red') #C II
plt.axvline(6891.39,linestyle='dotted',color='red') #He II


#Mercury Lines
'''plt.axvline(4340.47,linestyle='dotted',color='red') #H I
plt.axvline(4363.21,linestyle='dotted',color='red') #[O III]
plt.axvline(4685.68,linestyle='dotted',color='red') #He II
plt.axvline(4711.34,linestyle='dotted',color='red') #[Ne IV]
plt.axvline(4724.15,linestyle='dotted',color='red') #[Ne IV]
plt.axvline(4740.20,linestyle='dotted',color='red') #H[Ar IV]
plt.axvline(4861.33,linestyle='dotted',color='red') #H I
plt.axvline(4958.92,linestyle='dotted',color='red') #[O III]
plt.axvline(5006.84,linestyle='dotted',color='red') #[O III]
'''

ax2=plt.subplot(212)
ax2.plot(x,y)

ax2.yaxis.get_offset_text().set_visible(False)

plt.xlim([6200.0, 7000.0])
plt.tick_params(axis='x', labelsize=10)
plt.ylim([0, 1.0e-12])
plt.xlabel(r'Wavelength ($\AA$)', fontsize=14)
plt.ylabel(r'Flux (1e-13)', fontsize=14)
plt.minorticks_on()

plt.yticks( np.arange(0,1.0e-12,3.0e-13))

#Mercury Lines
'''plt.axvline(4340.47,linestyle='dotted',color='red') #H I
plt.axvline(4363.21,linestyle='dotted',color='red') #[O III]
plt.axvline(4685.68,linestyle='dotted',color='red') #He II
plt.axvline(4711.34,linestyle='dotted',color='red') #[Ne IV]
plt.axvline(4724.15,linestyle='dotted',color='red') #[Ne IV]
plt.axvline(4740.20,linestyle='dotted',color='red') #H[Ar IV]
plt.axvline(4861.33,linestyle='dotted',color='red') #H I
plt.axvline(4958.92,linestyle='dotted',color='red') #[O III]
plt.axvline(5006.84,linestyle='dotted',color='red') #[O III]
'''

#Neon Lines
plt.axvline(6233.94,linestyle='dotted',color='red') #He II
plt.axvline(6311.95,linestyle='dotted',color='red') #[S III]
plt.axvline(6406.45,linestyle='dotted',color='red') #He II
plt.axvline(6435.11,linestyle='dotted',color='red') #[Ar V]
plt.axvline(6548.03,linestyle='dotted',color='red') #[N II]
plt.axvline(6562.82,linestyle='dotted',color='red') #H I
plt.axvline(6583.41,linestyle='dotted',color='red') #[N II]
plt.axvline(6678.15,linestyle='dotted',color='red') #He I
plt.axvline(6716.47,linestyle='dotted',color='red') #[S II]
plt.axvline(6730.85,linestyle='dotted',color='red') #[S II]
plt.axvline(6780.14,linestyle='dotted',color='red') #C II
plt.axvline(6891.39,linestyle='dotted',color='red') #He II


plt.title(r'', fontsize=16)

plt.subplots_adjust(hspace=0)

plt.savefig('neon-plt.png', format='png',dpi=150)

plt.show()
