import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy import stats
from scipy.stats import norm

hdulist = fits.open("/home/icecube/AST/CGS-GroupData/lab0/BigCCD/biases-Neg5-Vis.00000000.BIAS.FIT")
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

mean = np.mean(countvalues)
sig = np.std(countvalues)

xarray = np.linspace(cmin,cmax,nbins*10)
yarray = normalization*norm.pdf(xarray,loc = mean,scale = sig)
#plt.hist(countvalues,range=[cmin,cmax],bins=nbins);
plt.yscale("log")
plt.ylim([0.1,1e6])
#plt.plot(xarray,yarray,color="red")
#plt.show()

cut_upper = mean+5*sig
cut_lower = mean-5*sig

clippedvalues = countvalues[(countvalues>=cut_lower) & (countvalues<=cut_upper)]
