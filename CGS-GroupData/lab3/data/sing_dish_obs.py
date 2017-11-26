import numpy as np
import matplotlib.pyplot as plt

sun_time = np.genfromtxt("Base-Single-70-00.txt",skip_header = 7,usecols = 0)
sun_pot = np.genfromtxt("Base-Single-70-00.txt",skip_header = 7,usecols = 1)
sat_time = np.genfromtxt("single_dish_sat1.csv",delimiter=',',usecols = 0)
sat_pot = np.genfromtxt("single_dish_sat1.csv",delimiter=',',usecols = 1)

sun_peak_val = np.max(sun_pot)
sat_peak_val = np.max(sat_pot)

sun_pot = sun_pot/sun_peak_val
sat_pot = sat_pot/sat_peak_val

plt.plot(sun_time,sun_pot,label = "sun")
plt.plot(sat_time,sat_pot,label = "sat")
plt.legend()
plt.show()

