import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import os

lorenapath = '/home/lmezini/AST443/CGS-GroupData/lab1/calibration2'
jasminepath = '/home/jgarani/AST443/CGS-GroupData/lab1/calibration2'

path = lorenapath

#create function to calcualte scaled flux and error
def flux_calc(flux,error):
    fscaled = flux/np.mean(flux)
    escaled = error/np.mean(flux) 
    return fscaled,escaled

#create lists to hold variables that we need to print for our science object
sciflux = []
scierr = []
sciname = []
dates =[]
filenames = []

#create lists of lists for variables for the 10 extra objects
names = [[] for _ in range(10)] #each list has 10 lists in it for each object
fref = [[] for _ in range(10)]
eref = [[] for _ in range(10)]

for f in os.listdir(path):
    #find our science object
    if "hd" in f and "txt" in f:
        #print f
        name = np.genfromtxt(str(path)+'/'+str(f),dtype = str,usecols = 0)
        RA = np.genfromtxt(str(path)+'/'+str(f),usecols = 1)
        DEC = np.genfromtxt(str(path)+'/'+str(f),usecols = 2)
        flux = np.genfromtxt(str(path)+'/'+str(f),usecols = 3)
        error = np.genfromtxt(str(path)+'/'+str(f),usecols = 4)
        
        star_fscaled = flux_calc(flux,error)[0]
        star_escaled = flux_calc(flux,error)[1]
        #open fits files to get time
        for i in range(len(name)):
            hdulist = fits.open(str(path)+'/'+str(name[i])[:-3]+'new',ignore_missing_end=True)
            header = hdulist[0].header
            date = header['DATE']
            dates.append(date)
            sciflux.append(star_fscaled[i])
            scierr.append(star_escaled[i])
            sciname.append(name[i])
    #get names of txt files for other objects
    if "time_flux" in f and "hd" not in f and '~' not in f:
        filenames.append(f)

i = 0
for f in filenames:
    #repeat process for extra objects
    name = np.genfromtxt(str(path)+'/'+str(f),dtype = str,usecols = 0)
    RA = np.genfromtxt(str(path)+'/'+str(f),usecols = 1)
    DEC = np.genfromtxt(str(path)+'/'+str(f),usecols = 2)
    flux = np.genfromtxt(str(path)+'/'+str(f),usecols = 3)
    error = np.genfromtxt(str(path)+'/'+str(f),usecols = 4)
    ref_fscaled, ref_escaled = flux_calc(flux,error) #scaled fluxes and errors for reference images
    j = 0
    #add values to list of lists
    for j in range(len(name)):
        names[i].append(name[j])
        fref[i].append(ref_fscaled[j])
        eref[i].append(ref_escaled[j])
        j = j +1
    i = i+1
    t_refstar = []
    
    for w in range(len(name)):
        t_refstar.append(w)
    plt.plot(t_refstar, ref_fscaled,label = str(f))
    plt.legend()
plt.show()

  
#create list for averaged flux and error over non-sci objects
us = []
uerrs = []

for k in range(len(names[1])):
    if names[1][k] == sciname[k]:
        #sum up scaled flux for other objects at specific times
        unum = (fref[1][k]/(eref[1][k]**2))+(fref[2][k]/(eref[2][k]**2))+(fref[3][k]/(eref[3][k]**2))+(fref[4][k]/(eref[4][k]**2))+(fref[5][k]/(eref[5][k]**2))+(fref[6][k]/(eref[6][k]**2))+(fref[7][k]/(eref[7][k]**2))+(fref[8][k]/(eref[8][k]**2))+(fref[0][k]/(eref[0][k]**2))
        udenom = (1.0/(eref[1][k]**2))+(1.0/(eref[2][k]**2))+(1.0/(eref[3][k]**2))+(1.0/(eref[4][k]**2))+(1.0/(eref[5][k]**2))+(1.0/(eref[6][k]**2))+(1.0/(eref[7][k]**2))+(1.0/(eref[8][k]**2))+(1.0/(eref[0][k]**2))
        uerr = np.sqrt(1.0/udenom) 
        us.append(unum/udenom)
        uerrs.append(uerr)
    else:
        print names[1][k],sciname[k]

print sciname[544]
t = []
for k in range(len(sciflux)):
    print dates[k],sciflux[k],scierr[k],us[k],uerrs[k],sciflux[k]/us[k]
for k in range(len(sciflux)):
    t.append(k)

plt.plot(t,sciflux)
plt.plot(t,us)
plt.ylim(0.8,1.10)
plt.show()
