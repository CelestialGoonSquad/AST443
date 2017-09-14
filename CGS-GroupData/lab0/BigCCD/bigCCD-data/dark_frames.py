import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy import stats
from scipy.stats import norm
import os

jasminepath = "/Users/Jasmine/Documents/stony_brook/y4_sb/ast443/CGS-Groupdata/lab0/BigCCD/bigCCD-data/"
lorenapath = "/home/icecube/AST/CGS-GroupData/lab0/BigCCD/bigCCD-data/"

#Plot and fit bias
def plotdark(path,exptime):
    if exptime == '300s':
        filename = 'darks-expos300s-Neg10-Vis.00000000.DARK.FIT'
    print lorenapath + '/' + filename
    hdulist = fits.open(lorenapath + '/' + filename)
    header = hdulist[0].header
    print(header)
    imagedata = hdulist[0].data
    countvalues = imagedata.flatten()
    print("max counts = " + str(np.max(countvalues)))
    print("min counts = " + str(np.min(countvalues)))

    print("mean = " + str(np.mean(countvalues)))
    print("mode = " + str(stats.mode(countvalues)[0][0]))
    print("median = " + str(np.median(countvalues)))
    print("sigma = " + str(np.std(countvalues)))
    
    #plt.hist(countvalues, bins = 100, range=[1000,1200], histtype = 'step')
    #plt.show()
    return

def gaussfit(path,exptime):
    if exptime == '300s':
        filename = 'darks-expos300s-Neg10-Vis.00000000.DARK.FIT'
    print lorenapath + '/' + filename
    hdulist = fits.open(lorenapath + '/' + filename)
    imagedata = hdulist[0].data
    countvalues = imagedata.flatten()
    cmin = 950
    cmax = 1150
    nbins = 100

    normalization = ((cmax-cmin)/nbins)*len(countvalues[(countvalues>=cmin) & (countvalues<=cmax)])
    mean_single = np.mean(countvalues) #mean of single image
    sig_single = np.std(countvalues[countvalues<=cmax]) #standard deviation of single image

    #fit gaussian
    xarray = np.linspace(cmin,cmax,nbins*10)
    yarray = normalization*norm.pdf(xarray,loc = mean_single,scale = sig_single)
    plt.hist(countvalues,range=[cmin,cmax],bins=nbins, histtype = 'step');
    plt.plot(xarray,yarray,color="red")
    plt.yscale('log')
    plt.ylim([0.1,1e6])
    plt.show()

    #set cut limimts for outliers
    cut_upper = mean_single+5*sig_single
    cut_lower = mean_single-5*sig_single

    clippedvalues = countvalues[(countvalues>=cut_lower) & (countvalues<=cut_upper)]

    #calculate percent of pixels rejected by cut
    pix_reject = 100*((len(countvalues)-len(clippedvalues))/float(len(countvalues)))
    print("percent of pixels rejected = "+str(pix_reject))
    print("clipped mean = " + str(np.mean(clippedvalues)))
    print("clipped mode = " + str(stats.mode(clippedvalues)[0][0]))
    print("clipped median = " + str(np.median(clippedvalues)))
    print("clipped sigma = " + str(np.std(clippedvalues)))

    #Identify hot/warm pixels as those greater than 5 sigma
    

plotdark(lorenapath, "300s")
gaussfit(lorenapath, "300s")
