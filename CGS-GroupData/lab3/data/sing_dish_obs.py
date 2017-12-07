import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

#Sun Position at T = 15:05:00 is Alt 13.4 and Az 230.1
#Sat is located at Alt 45

sun_time = np.genfromtxt("Base-Single-70-00.txt",skip_header = 7,usecols = 0)
sun_pot = -1.*np.genfromtxt("Base-Single-70-00.txt",skip_header = 7,usecols = 1)
sat_time = np.genfromtxt("sat3_single_2.txt",usecols = 0)
sat_pot = -1.*np.genfromtxt("sat3_single_2.txt",usecols = 1)

sun_base = np.mean(sun_pot[-10:-1])
sat_base = np.mean(sat_pot[-10:-1])
sun_base_err = np.std(sun_pot[-10:-1])
sat_base_err = np.std(sat_pot[-10:-1])

sun_pot = sun_pot - sun_base
sat_pot = sat_pot - sat_base

el_rat = np.cos(44.1*np.pi/180.)/np.cos(13.4*np.pi/180.)
sun_time = sun_time/el_rat

sun_peak_val = np.max(sun_pot)
sat_peak_val = np.max(sat_pot)

sun_pot = sun_pot/sun_peak_val
sat_pot = sat_pot/sat_peak_val

j_sun = np.where(sun_pot == np.max(sun_pot))
j_sat = np.where(sat_pot == np.max(sat_pot))
t_diff = sun_time[j_sun] - sat_time[j_sat]
sat_time = sat_time + t_diff

#find FWHM
half_sun_pot = np.max(sun_pot)/2.
sun_half_t = []
for i in range(len(sun_pot)):
    if sun_pot[i] >= half_sun_pot-0.02 and sun_pot[i] <= half_sun_pot+0.02:
        sun_half_t.append(sun_time[i])

half_sat_pot = np.max(sat_pot)/2.
sat_half_t = []
for i in range(len(sat_pot)):
    if sat_pot[i] >= half_sat_pot-0.02 and sat_pot[i] <= half_sat_pot+0.02:
        sat_half_t.append(sat_time[i])

FWHM_sun = sun_half_t[2] - sun_half_t[0]
FWHM_sat = sat_half_t[1] - sat_half_t[0]
print "FWHM_sun: " + str(FWHM_sun)
print "FWHM_sat: " + str(FWHM_sat)


plt.plot(sun_time,sun_pot,label = "sun")
plt.plot(sat_time,sat_pot,label = "sat")
plt.legend()
plt.show()

