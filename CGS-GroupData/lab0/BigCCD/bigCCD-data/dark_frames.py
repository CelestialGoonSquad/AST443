#Jasmine Garani, Lorena Mezini, Patrick Payne
#Code for dealing with dark frames (4.2 of lab 0)
#"Decide how to identify hot pixels and warm pixels. What fraction of the CCD does each category make up" -- not in this code, done in badpixmap.py 


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy import stats
from scipy.stats import norm
import os

jasminepath = "/Users/Jasmine/Documents/stony_brook/y4_sb/ast443/CGS-Groupdata/lab0/BigCCD/bigCCD-data/"
lorenapath = "/home/icecube/AST/CGS-GroupData/AST443/CGS-GroupData/lab0/BigCCD/bigCCD-data/"

#Plot and fit bias
def plotdark(path,exptime,temp):
    if exptime == '300s' and temp == 'Neg10':
        filename = 'darks-expos300s-Neg10-Vis.00000000.DARK.FIT'
    if exptime == '300s' and temp == 'Neg5':
        filename = 'darks-expos300s-Neg5-Vis.00000000.DARK.FIT'
    #print lorenapath + '/' + filename
    hdulist = fits.open(path + '/' + filename)
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
    
    plt.hist(countvalues, bins = 100, range=[1000,1200], histtype = 'step')
    plt.show()
    return

def gaussfit(path,exptime,temp):
    if exptime == '300s' and temp == 'Neg10':
        filename = 'darks-expos300s-Neg10-Vis.00000000.DARK.FIT'
    if exptime == '300s' and temp == 'Neg5':
        filename = 'darks-expos300s-Neg5-Vis.00000000.DARK.FIT'
    #print lorenapath + '/' + filename
    hdulist = fits.open(path + '/' + filename)
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
    #plt.show()

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

def DarkCurrent(path,temp,master):
    t = []
    counts = []
    for f in os.listdir(path):
        if "DARK" in f and temp in f:
            dark_hdulist = fits.open(path + '/' + f)
            dark_imageheader = dark_hdulist[0].header
            dark_imagedata = dark_hdulist[0].data
            mast_hdulist = fits.open(path + '/' + master)
            mast_imagedata = mast_hdulist[0].data
            dark_current = dark_imagedata.flatten() - mast_imagedata.flatten()
            
            mode = stats.mode(dark_current)[0][0]
            median = np.median(dark_current) #we have decided to use median not mode because of how gaussain looks
            counts.append(median)
            print("mode for " + str(f) + " = " + str(mode))
            print(median)
            t.append(dark_imageheader['EXPTIME'])
    print t
    plt.plot(t,counts,marker='o',linestyle='none')
    coef = np.polyfit(t,counts,1)
    fit = np.poly1d(coef)
    print fit #slope the dark current in electrons per pixel per second
    x = np.linspace(0,300.0,100)
    plt.plot(x,fit(x))
    plt.xlabel(r'Exposure Time (s)')
    plt.ylabel(r'Counts')
    plt.title(r'Dark Current at -5$\degree$C')
    linregression = linregress(t,counts)
    print "Standard Error:", linregression.stderr
    plt.show()
    plt.savefig(path + '/' + 'dark-current5.png',format='png')
#plotdark(jasminepath, "300s",'Neg5')
plotdark(jasminepath, "300s", 'Neg10')
#gaussfit(jasminepath, "300s",'Neg5')
#gaussfit(jasminepath, "300s',"Neg10")
#DarkCurrent(jasminepath, "Neg5","master-bias-Neg5.fits")
#DarkCurren(jasminepath, "Neg10","master-bias-Neg10.fits")
