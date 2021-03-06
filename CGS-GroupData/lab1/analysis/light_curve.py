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
sciflux = []            #flux on the science object
scierr = []             #error on the flux of the science object
sciname = []            #array of science files to be used
dates =[]
filenames = []          #array of files to be used
ignore = [23,26,76]         #array for lines to be ignored due to deviation
fluxpretran = []        #array of flux values for images before transit
errpretran = []         #error in the flux values prior to transit
fluxaftertran = []      #array of flux values for images after transit
erraftertran = []       #error in the flux values post transit
totfluxforbase = []     #all flux values not in the transit
errtotfluxforbase = []  #error in flux values not in transt
fluxtran = []           #flux values during transity
errtran = []            #error in flux values during transity
#t_refstar = []          #array of number of reference star files
times = []              #array of the time of for a observation file
mus = []                #weighted normalized average for reference stars
muerrs = []             #weighted error for weighted averages of reference stars
ri = []                 #normalized and corrected flux for science object
errris = []             #error for normalized,corrected flux
binedData = []          #place where data goes after it is bined
binedError = []         #array of errors for bined values
bins = []               #makes bin by bin number
binedTime = []          #array of time at the center of a bin
pre_trans = []          #array of normalized flux pre transit
trans = []              #array of normalized flux during transity
post_trans = []         #array of normalized flux post tranist
t = []                  #array of file numbers for plotting




#create lists of lists for variables for the 10 extra objects
names = [[] for _ in range(10)] #each list has 10 lists in it for each object
fref = [[] for _ in range(10)]
eref = [[] for _ in range(10)]

for f in os.listdir(path):
    #find our science object
    if "hd" in f and "txt" in f:
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
            scierr.append(error[i])
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
    for j in range(len(name)):        
        if ref_fscaled[j] < 0.4 or ref_fscaled[j] > 1.1:
            if j not in ignore:                
                ignore.append(j)
        names[i].append(name[j])
        fref[i].append(ref_fscaled[j])
        eref[i].append(ref_escaled[j])


    i = i+1
    t_refstar = []
    for w in range(len(name)):
        t_refstar.append(w)

    t_refstar = np.delete(t_refstar,ignore)
    ref_fscaled = np.delete(ref_fscaled,ignore)


#Calculate the times, put everything into seconds
#times = []
first = 0
for w in names[0]:
    new = w.replace('.cat','.FIT')
    fortimehdulist = fits.open(path + '/' + new)
    fortimeheader = fortimehdulist[0].header
    indtime = fortimeheader['TIME-OBS']
    htos = int(indtime[0:2]) * 3600.
    mtos = int(indtime[3:5]) * 60.
    sec = float(indtime[6:])
    totsec = htos+mtos+sec
    if first == 0:
        firsttime = totsec
        totsec = totsec - firsttime
        first = 1
    else:
        totsec = totsec - firsttime
    times.append(totsec)

for i in range(0,len(sciflux)):
#    if sciflux[i] > 225500:
#        if i not in ignore:
#            ignore.append(i)
    if sciflux[i] < 192000:
        if i not in ignore:
            ignore.append(i)
    elif i < 480 and i > 455 and sciflux[i] < 202200:
        if i not in ignore:
            ignore.append(i)
    elif i < 428 and sciflux[i] < 206000:
        if i not in ignore:
            ignore.append(i)

# removes the problem images... we've already dealt with the children :)
#times = np.delete(times,ignore)
for k in range(0,10):
    names[k] = np.delete(names[k],ignore)
    fref[k] = np.delete(fref[k],ignore)
    eref[k] = np.delete(eref[k],ignore)

for i in range(0,len(ignore)):
    if ignore[i] < index177:
        index177 = index177 + 1
        if ignore[i] < index503:
            index503 = index503 + 1
        else:
            pass
    else:
        pass


#open fits files to get time
for i in range(len(sciflux)):
    if i <= index177: 
        fluxpretran.append(sciflux[i])
        errpretran.append(error[i])
        totfluxforbase.append(sciflux[i])
        errtotfluxforbase.append(error[i])
    elif i >= index503:
        fluxaftertran.append(sciflux[i])
        erraftertran.append(error[i])
        totfluxforbase.append(sciflux[i])
        errtotfluxforbase.append(error[i])
    elif i < 420 and i > 292:
        fluxtran.append(sciflux[i])
        errtran.append(error[i])


tranline = np.mean(fluxtran)
errtranbase = np.std(fluxtran,ddof=1)/np.sqrt(len(fluxtran))
baseline = np.mean(totfluxforbase)
errbase = np.std(totfluxforbase,ddof=1)/np.sqrt(len(totfluxforbase))
print "baseline and error: ", baseline,errbase
print "tranline and error: ", tranline,errtranbase


sciflux = np.delete(sciflux,ignore)
sciname = np.delete(sciname,ignore)
scierr = np.delete(scierr,ignore)


#create list for averaged flux and error over non-sci objects
#mus = []
#muerrs = []
#ri = []
#errris = []

for k in range(len(names[1])):
    if names[1][k] == sciname[k]:
        #sum up scaled flux for other objects at specific times
        munum = (fref[1][k]/(eref[1][k]**2))+(fref[2][k]/(eref[2][k]**2))+(fref[3][k]/(eref[3][k]**2))+(fref[4][k]/(eref[4][k]**2))+(fref[5][k]/(eref[5][k]**2))+(fref[6][k]/(eref[6][k]**2))+(fref[7][k]/(eref[7][k]**2))+(fref[8][k]/(eref[8][k]**2))+(fref[0][k]/(eref[0][k]**2))
        mudenom = (1.0/(eref[1][k]**2))+(1.0/(eref[2][k]**2))+(1.0/(eref[3][k]**2))+(1.0/(eref[4][k]**2))+(1.0/(eref[5][k]**2))+(1.0/(eref[6][k]**2))+(1.0/(eref[7][k]**2))+(1.0/(eref[8][k]**2))+(1.0/(eref[0][k]**2))
        muerr = np.sqrt(1.0/mudenom) 
        mus.append(munum/mudenom)
        muerrs.append(muerr)
    else:
        pass

#baseline=1.0

for i in range(len(sciflux)):  # calculates normalized ri
    divtemp = sciflux[i]/(mus[i]*baseline)
    ri.append(divtemp)
    partialsciflux = scierr[i]/(mus[i]*baseline)
    partialmu = -(muerrs[i]*sciflux[i])/((mus[i])**2 * baseline)
    partialbaseline = -(errbase*sciflux[i])/(mus[i]*baseline**2)
    errri = np.sqrt(partialsciflux**2 + partialmu**2 + partialbaseline**2)
    errris.append(errri)

for i in range(0,len(ri)):
    if ri[i] > 1.01:
        if i not in ignore:
            ignore.append(i)

ri = np.delete(ri,ignore)
times = np.delete(times,ignore)
# Binning of the data

userBinSize = 300 #Length of each bin in seconds
imagesInBin = userBinSize // 20
if imagesInBin <= 0:
    imagesInBin = 1
actualBinSize = imagesInBin * 20
numBins = len(ri)//imagesInBin
last_bin = len(ri) % imagesInBin
average = []



for i in range(0,numBins):  #calculates the value for each bin according to bin size
    sum = 0
    start = i*imagesInBin          #bin boundaries
    end = ((i+1)*imagesInBin) - 1
    for k in range(start,end):
        average.append(ri[k])
    binedData.append(np.mean(average))      # value for a bin
    binedError.append(np.std(average)/np.sqrt(imagesInBin))
    average = []
    if i == numBins  and last_bin > 0:   #calculation if bins dont cover all ri values
        last_bin_left = end + 1
        last_bin_right = end + last_bin
        for k in range (last_bin_left,last_bin_right):
            sum = ri[k] + sum
        lastavg = sum / last_bin
        binedData.append(lastavg)
        
#bins = [] #makes bin by bin number
for i in range(0,(numBins)):
    bins.append(i)

#do the bining stuff for the times now
#binedTime = []
for i in range(0,numBins):   #calculates the value for each bin according to bin size
    start = i*imagesInBin     #bin boundaries
    end = ((i+1)*imagesInBin) - 1
    binedTimei = (times[start] + times[end])/2.
    binedTime.append(binedTimei)

#Determine the transit depth

pre_trans = []
trans = []
post_trans = []

index177=187
index503=451

for i in range (0,numBins):
    if binedTime[i] < times[index177]:
        pre_trans.append(binedData[i]) #builds array of pre transit normalized flux
    elif binedTime[i] > times[index503]:
        post_trans.append(binedData[i]) #builds array of post transit normalized flux
    elif binedTime[i] < times[360] and binedTime[i] > times[310]:
        trans.append(binedData[i])      #builds array of transit normalized flux

avg_pre   = np.mean(pre_trans)
err_pre   = np.std(pre_trans)/np.sqrt(len(pre_trans))
avg_trans = np.mean(trans)
err_trans = np.std(trans)/np.sqrt(len(trans))
avg_post  = np.mean(post_trans)
err_post  = np.std(post_trans)/np.sqrt(len(post_trans))

avg_non_trans = (avg_pre + avg_post)/2.0
err_non_trans = np.sqrt(err_pre**2.0 + err_post**2.0)/np.sqrt(2.0)

depth =  avg_non_trans - avg_trans 
err_depth = np.sqrt(err_non_trans**2 + err_trans**2)
depth_prcnt = (depth/avg_non_trans) * 100.
pt1 = err_depth/avg_non_trans 
pt2 = (err_non_trans*depth)/avg_non_trans**2.0
err_prcnt = np.sqrt(pt1**2 + pt2**2)
print "Transit Depth: ", depth, err_depth
print "Transit Depth %: ",depth_prcnt, err_prcnt

# Planet star radius ratio
# equation for ratio r/R = sqrt( 1 - transit flux / baseline flux)

f2 = avg_trans
err_f2 = err_trans
f1 = avg_non_trans
err_f1 = err_non_trans
print "f1 = ", f1, err_f1
print "f2 = ", f2, err_f2
division = f2/f1

ratio_squared = 1 - (f2/f1)
ratio = np.sqrt(ratio_squared)

part_err_ratio_sq = (err_f2/f1)
part2_err_ratio_sq= ((f2*err_f1)/(f1**2))
err_ratio_squared = np.sqrt( part_err_ratio_sq**2 + part2_err_ratio_sq**2)
err_ratio = 0.5 * err_ratio_squared * np.sqrt(1/ratio)

print "Planet Star radius ratio", ratio, err_ratio



# I/O stuffs
#t = []
for k in range(len(sciflux)):
    #print k,dates[k],sciflux[k],scierr[k],mus[k],muerrs[k],sciflux[k]/mus[k]
    pass
for k in range(len(sciflux)):
    t.append(k)

#textfile = open("records.txt","rw")
#for files in range(0,len(sciflux)):
#    textfile.write(sciflux[files] + "    " + scierr[files] + "    "  + mus[files] + "    " + ri[files])

t = np.delete(t,ignore)

#Plotting Jazz! Doobie do bop, groovie!!
spacespace = np.linspace(0,max(mus),len(mus))    
plt.plot(binedTime,binedData,linestyle='none',marker='o',label = 'HD 189733')
plt.errorbar(binedTime,binedData,yerr=binedError,linestyle='none',capsize=3,color='black')
#plt.plot(bins,binedData,linestyle = "none",marker='o')
#plt.plot(t,ri,linestyle = "none",marker='x')
#plt.plot(t,mus)
#plt.plot(t_refstar,ref_fscaled,linestyle='none',marker='o',label= "Reference Star")
#plt.errorbar(t_refstar,ref_fscaled,yerr=ref_escaled,linestyle='none',capsize=3,color='black')
#plt.ylim(0.8,1.10)
plt.xlabel(r'Time (s)', fontsize=12)
plt.ylabel(r'Relative Flux', fontsize=12)
plt.legend(loc=1)
plt.savefig('transit-hd189733.pdf',format='pdf')
plt.show()
