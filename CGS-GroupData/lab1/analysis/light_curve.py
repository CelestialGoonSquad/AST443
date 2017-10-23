Aimport numpy as np
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
fluxaftertran = []
erraftertran = []
totfluxforbase = []
errtotfluxforbase = []

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
                totfluxforbase.append(flux[i])
                errtotfluxforbase.append(error[i])
            if i >= index503:
                fluxaftertran.append(flux[i])
                erraftertran.append(error[i])
                totfluxforbase.append(flux[i])
                errtotfluxforbase.append(error[i])
            scierr.append(error[i])
            sciname.append(name[i])
    #get names of txt files for other objects
    if "time_flux" in f and "hd" not in f and '~' not in f:
        filenames.append(f)

print len(totfluxforbase)
baseline = np.mean(totfluxforbase)
#errbase = np.mean(errpretran) #not the right way to do it I don't think 
errbase = np.std(totfluxforbase,ddof=1)/np.sqrt(len(totfluxforbase))
print "baseline and error: ", baseline,errbase

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

    print 'length of t_refstar after = ', len(t_refstar)
    # removes problem children...actually just the problem images
    t_refstar = np.delete(t_refstar,ignore)
    ref_fscaled = np.delete(ref_fscaled,ignore)
    #plt.plot(t_refstar, ref_fscaled,label = str(f))
    #plt.legend()
#plt.show()
print 'length of t_refstar before = ', len(t_refstar)



#Calculate the times, put everything into seconds
times = []
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

# removes the problem images... we've already dealt with the children :)
times = np.delete(times,ignore)
sciflux = np.delete(sciflux,ignore)
sciname = np.delete(sciname,ignore)
scierr = np.delete(scierr,ignore)
for k in range(0,10):
    names[k] = np.delete(names[k],ignore)
    fref[k] = np.delete(fref[k],ignore)
    eref[k] = np.delete(eref[k],ignore)


#create list for averaged flux and error over non-sci objects
mus = []
muerrs = []
ri = []
errris = []

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
    partialsciflux = scierr[i]/(mus[i]*baseline)
    partialmu = -(muerrs[i]*sciflux[i])/((mus[i])**2 * baseline)
    partialbaseline = -(errbase*sciflux[i])/(mus[i]*baseline**2)
    errri = np.sqrt(partialsciflux**2 + partialmu**2 + partialbaseline**2)
    errris.append(errri)
print 'len(errris) = ', len(errris)
print 'errris = ', errris

# Binning of the data

binedData = []    #place where data goes after it is bined
userBinSize = 200 #Length of each bin in seconds
imagesInBin = userBinSize // 20
if imagesInBin <= 0:
    imagesInBin = 1
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
        last_bin_left = end + 1
        last_bin_right = end + last_bin
        for k in range (last_bin_left,last_bin_right):
            sum = ri[k] + sum
        lastavg = sum / last_bin
        binedData.append(lastavg)
        
bins = [] #makes bin by bin number
for i in range(0,(numBins)):
    bins.append(i)

#do the bining stuff for the times now
binedTime = []
for i in range(0,numBins):   #calculates the value for each bin according to bin size
    start = i*imagesInBin     #bin boundaries
    end = ((i+1)*imagesInBin) - 1
    binedTimei = (times[start] + times[end])/2.
    binedTime.append(binedTimei)
print 'binedTime array = ', binedTime
print 'len of binedTime array = ', len(binedTime)

#Determine the transit depth

pre_trans = []
trans = []
post_trans = []

for i in range (0,numBins):
    if binedTime[i] < times[177]:
        pre_trans.append(binedData[i]) #builds array of pre transit normalized flux
    elif binedTime[i] > times[503]:
        post_trans.append(binedData[i]) #builds array of post transit normalized flux
    else:
        trans.append(binedData[i])      #builds array of transit normalized flux

avg_pre   = np.mean(pre_trans)
avg_trans  = np.mean(trans)
avg_post  = np.mean(post_trans)

avg_non_trans = (avg_pre + avg_post)/2.0

depth =  avg_non_trans - avg_trans
depth_prcnt = (depth/avg_non_trans) * 100.
print "Transit Depth: ", depth
print "Transit Depth %: ",depth_prcnt
# Other potential methods, not sure which is actually the best representation

depth1 = avg_pre - avg_trans
depth1_prcnt = (depth1/avg_pre) * 100.
print "Depth Method 2 (depth,%): ", depth1, depth1_prcnt
depth2 = avg_post - avg_trans
depth2_prcnt = (depth2/avg_post) * 100
print "Depth Method 2 (depth,%): ", depth2, depth2_prcnt

#Determine error in transit depth

# -----------------------???


# I/O stuffs
t = []
for k in range(len(sciflux)):
    #print k,dates[k],sciflux[k],scierr[k],mus[k],muerrs[k],sciflux[k]/mus[k]
    pass
for k in range(len(sciflux)):
    t.append(k)


#Plotting Jazz! Doobie do bop, groovie!!
    
plt.plot(binedTime,binedData,linestyle='none',marker='o',label = 'HD 189733')
plt.errorbar(binedTime,binedData,yerr=errri,linestyle='none',color='black')
#plt.plot(bins,binedData,linestyle = "none",marker='o')
#plt.plot(t,ri,linestyle = "none",marker='x')
#plt.plot(t,mus)
#plt.ylim(0.8,1.10)
plt.xlabel(r'Times Elapsed (s)', fontsize=12)
plt.ylabel(r'Relative Flux', fontsize=12)
plt.legend(loc=1)
plt.show()
