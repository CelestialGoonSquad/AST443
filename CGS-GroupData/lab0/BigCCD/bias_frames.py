import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy import stats
from scipy.stats import norm
import os

jasminepath = "/Users/Jasmine/Documents/stony_brook/y4_sb/ast443/CGS-Groupdata/lab0/BigCCD/bigCCD-data/"
hdulist = fits.open(jasminepath + '/' + "biases-Neg5-Vis.00000000.BIAS.FIT")
header = hdulist[0].header
#print(header)
imagedata = hdulist[0].data
countvalues = imagedata.flatten()
print("max counts = " + str(np.max(countvalues)))
print("min counts = " + str(np.min(countvalues)))

print("mean = " + str(np.mean(countvalues)))
print("mode = " + str(stats.mode(countvalues)[0][0]))
print("median = " + str(np.median(countvalues)))
print("sigma = " + str(np.std(countvalues)))

cmin = 900
cmax = 1200
nbins = 100

normalization = (cmax-cmin)/nbins*len(countvalues[(countvalues>=cmin) & (countvalues<=cmax)])

mean_single = np.mean(countvalues) #mean of single image
sig_single = np.std(countvalues) #standard deviation of single image

xarray = np.linspace(cmin,cmax,nbins*10)
yarray = normalization*norm.pdf(xarray,loc = mean_single,scale = sig_single)
#plt.hist(countvalues,range=[cmin,cmax],bins=nbins);
plt.yscale("log")
plt.ylim([0.1,1e6])
#plt.plot(xarray,yarray,color="red")
#plt.show()

cut_upper = mean_single+5*sig_single
cut_lower = mean_single-5*sig_single

clippedvalues = countvalues[(countvalues>=cut_lower) & (countvalues<=cut_upper)]


#=============================================================================================
#4.1.3
#make master bias, find mean and std
def mastbineg5(path,temp): #path,temperature word in file name
    all_bias = []
    for f in os.listdir(jasminepath):
        if "bias" in f and temp in f: #put all biases in an array
            hdulist1 = fits.open(jasminepath + '/' + f)
            header1 = hdulist1[0].header
            imagedata1 = hdulist1[0].data
            all_bias.append(imagedata1)
    master_bias = np.mean(all_bias,axis=0)
    #newhdu = fits.PrimaryHDU(master_bias)
    #newhdu.writeto('master_bias.fits')
    countvalues1 = master_bias.flatten()
    mean_all = no.mean(countvalues1)
    sig_all = np.std(countvalues1)
    
    

    return



mastbineg5(jasminepath,"Neg5")
