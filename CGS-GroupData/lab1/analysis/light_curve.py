import numpy as np
import math
import matplotlib.pyplot as plt
from astropy.io import fits
import os

patpath = '/Users/ilovealltigers/SBU_F17/AST_443/LAB1/CGS-GroupData/lab1/calibration2'
lorenapath = '/home/lmezini/AST443/CGS-GroupData/lab1/calibration2'
jasminepath = '/home/jgarani/AST443/CGS-GroupData/lab1/calibration2'

path = jasminepath

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
ignore = []         #array for lines to be ignored due to deviation
fluxpretran = []
errpretran = []

#create lists of lists for variables for the 10 extra objects
names = [[] for _ in range(10)] #each list has 10 lists in it for each object
fref = [[] for _ in range(10)]
eref = [[] for _ in range(10)]

for f in os.listdir(path):
    #find our science object
    if "hd" in f and "txt" in f:
        #print f
        name = np.genfromtxt(str(path)+'/'+str(f),dtype = str,usecols = 0)
        index177 = np.where(name == 'bdf-L1-sci.00000177.cat')
        index177 = index177[0][0] # gets index of last file before transit
        index503 = np.where(name == 'bdf-L1-sci.00000503.cat')
        index503 = index503[0][0] # gets index of first file after transit
        RA = np.genfromtxt(str(path)+'/'+str(f),usecols = 1)
        DEC = np.genfromtxt(str(path)+'/'+str(f),usecols = 2)
        flux = np.genfromtxt(str(path)+'/'+str(f),usecols = 3)
        error = np.genfromtxt(str(path)+'/'+str(f),usecols = 4)
        
        #open fits files to get time
        for i in range(len(name)):
            hdulist = fits.open(str(path)+'/'+str(name[i])[:-3]+'new',ignore_missing_end=True)
            header = hdulist[0].header
            date = header['DATE']
            dates.append(date)
            sciflux.append(flux[i])
            if i <= index177: 
                fluxpretran.append(flux[i])
                errpretran.append(error[i])
            scierr.append(error[i])
            sciname.append(name[i])
    #get names of txt files for other objects
    if "time_flux" in f and "hd" not in f and '~' not in f:
        filenames.append(f)

baseline = np.mean(fluxpretran)
errbase = np.mean(errpretran)
#print "baseline and error: ", baseline,errbase

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
    for j in range(len(name)):        
#        if ref_fscaled[j] < (1.0 - 10*ref_escaled[j]) or ref_fscaled[j] > (1.0 + 10*ref_escaled[j]):
        if ref_fscaled[j] < 0.8 or ref_fscaled[j] > 1.2:
            if j not in ignore:                
                ignore.append(j)
        names[i].append(name[j])
        fref[i].append(ref_fscaled[j])
        eref[i].append(ref_escaled[j])
        j = j+1

    i = i+1
    t_refstar = []
    for w in range(len(name)):
        t_refstar.append(w)


    # removes problem children...actually just the problem images
    t_refstar = np.delete(t_refstar,ignore)
    ref_fscaled = np.delete(ref_fscaled,ignore)
    #plt.plot(t_refstar, ref_fscaled,label = str(f))
    #plt.legend()
#plt.show()

# removes the problem images... we've already dealt with the children :)
sciflux = np.delete(sciflux,ignore)
sciname = np.delete(sciname,ignore)
for k in range(0,10):
    names[k] = np.delete(names[k],ignore)
    fref[k] = np.delete(fref[k],ignore)
    eref[k] = np.delete(eref[k],ignore)


#create list for averaged flux and error over non-sci objects
mus = []
muerrs = []
ri = []


for k in range(len(names[1])):
    if names[1][k] == sciname[k]:
        #sum up scaled flux for other objects at specific times
        munum = (fref[1][k]/(eref[1][k]**2))+(fref[2][k]/(eref[2][k]**2))+(fref[3][k]/(eref[3][k]**2))+(fref[4][k]/(eref[4][k]**2))+(fref[5][k]/(eref[5][k]**2))+(fref[6][k]/(eref[6][k]**2))+(fref[7][k]/(eref[7][k]**2))+(fref[8][k]/(eref[8][k]**2))+(fref[0][k]/(eref[0][k]**2))
        mudenom = (1.0/(eref[1][k]**2))+(1.0/(eref[2][k]**2))+(1.0/(eref[3][k]**2))+(1.0/(eref[4][k]**2))+(1.0/(eref[5][k]**2))+(1.0/(eref[6][k]**2))+(1.0/(eref[7][k]**2))+(1.0/(eref[8][k]**2))+(1.0/(eref[0][k]**2))
        muerr = np.sqrt(1.0/mudenom) 
        mus.append(munum/mudenom)
        muerrs.append(muerr)
    else:
        #print names[1][k],sciname[k]
        pass
for i in range(len(sciflux)):  # calculates normalized ri
    divtemp = sciflux[i]/(mus[i]*baseline)
    ri.append(divtemp)


# Binning of the data

binedData = []    #place where data goes after it is bined
userBinSize = 300 #Length of each bin in seconds
imagesInBin = userBinSize // 20
actualBinSize = imagesInBin * 20
numBins = len(ri)//imagesInBin
last_bin = len(ri) % imagesInBin

for i in range(0,numBins):  #calculates the value for each bin according to bin size
    sum = 0
    start = i*imagesInBin          #bin boundaries
    end = ((i+1)*imagesInBin) - 1
    for k in range(start,end):
        sum = ri[k] + sum
    average = sum / imagesInBin
    binedData.append(average)      # value for a bin
    if i == numBins  and last_bin > 0:   #calculation if bins dont cover all ri values
        for k in range (0,last_bin):
            sum = ri[k] + sum
        lastavg = sum / last_bin
        binedData.append(lastavg)
        
print len(ri)
print numBins,imagesInBin,actualBinSize
bins = []
for i in range(0,(numBins+1)):
    bins.append(i)
print "Bined Data: ", binedData
print "bins: ", bins

# I/O stuffs
t = []
for k in range(len(sciflux)):
    #print k,dates[k],sciflux[k],scierr[k],mus[k],muerrs[k],sciflux[k]/mus[k]
    pass
for k in range(len(sciflux)):
    t.append(k)

plt.plot(bins,binedData,linestyle = "none",marker='o')
#plt.plot(t,ri,linestyle = "none",marker='x')
#plt.plot(t,mus)
#plt.ylim(0.8,1.10)
plt.show()
