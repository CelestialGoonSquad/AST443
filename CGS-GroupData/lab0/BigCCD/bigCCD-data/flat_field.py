#Jasmine Garani, Patrick Payne, Lorena Mezini
#Start date 9/13/17
#TEST
import numpy as np
from astropy.io import fits
import os
import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore',category=AstropyWarning)
import matplotlib.pyplot as plt
from scipy.stats import norm
#==========================================================================

jasminepath = "/Users/Jasmine/Documents/stony_brook/y4_sb/ast443/CGS-Groupdata/lab0/BigCCD/bigCCD-data/"

def masterflat(path):
    all_flats = []
    #hdulist1 = fits.open(jasminepath + '/' + 'flat-expos23s-Neg5-Vis.00000009.FIT', ignore_missing_end=True)
    for f in os.listdir(jasminepath):
        if "flat" in f and "FIT" in f:
            print f
            hdulist = fits.open(jasminepath + '/' + f,ignore_missing_end=True)
            header = hdulist[0].header
            imagedata = hdulist[0].data
            norm_data = imagedata/np.median(imagedata)
            all_flats.append(norm_data)
    master_flat = np.median(all_flats,axis=0)
    master_flat = master_flat/np.mean(master_flat)
    countvalues1 = master_flat.flatten()
    std = np.std(countvalues1)
    mean = np.mean(countvalues1)
    print mean - 5.*std

    for i in range(0,len(master_flat[0])):
        for k in range(0,len(master_flat[1])):
            if master_flat[i][k] <= mean - 5.*std:
                print i,k
    #flathdu = fits.PrimaryHDU(master_flat)
    #flathdu.writeto('master_flat.fits',clobber=True)
    low_counts = 0.956508
    high_counts = 1.03464
    ratio = low_counts/high_counts
    print ratio
    countvalues = master_flat.flatten()
    nbins = 100
    '''plt.hist(countvalues,bins=nbins)
    plt.yscale("log")
    plt.xlim([0.8,1.2])
    plt.show()'''


#find the gain of the CCD using a flat
def gain(path):
    hdulist2 = fits.open(path + '/' + 'flat-expos23s-Neg5-Vis.00000000.FIT') #get info of one header
    header2 = hdulist2[0].header
    imagedata2 = hdulist2[0].data
    countvalues2 = imagedata2.flatten()
    nbins = 100
    #plt.xlim([17000,25000.2])
    mu = 19738.0
    stdt = 375.991
    #x2 = np.arange(17000,25000,0.001)
    #plt.plot(x2,norm.pdf(x2,mu,stdt),label='Gaussian')
    
    lower_bound = 440 #get center out of flat
    upper_bound = 580
    centerbox = np.zeros((140,140))
    for i in range(lower_bound,upper_bound):
        for k in range(lower_bound,upper_bound):
            centerbox[i-lower_bound][k-upper_bound] = imagedata2[i][k]
    boxhdu = fits.PrimaryHDU(centerbox)
    boxhdu.writeto('boxflat.fits',clobber=True)
    boxflatten = centerbox.flatten()
    plt.hist(boxflatten,bins=nbins)
    plt.yscale("log")


    '''x=np.linspace(17000,25000,1000)
    mu = 19738.0
    sig = 375.991
    y=(1/(sig*np.sqrt(2*np.pi)))*np.exp((-1.0*(x-mu)**2)/(2*sig**2))

    plt.plot(x,y,label='\mu,\sigma=30,\sqrt{30}')
    plt.legend(loc=0) #Places Legend                                             
    plt.grid(True)
    
    plt.show()
    meanb = np.mean(countvalues2) #calculate mean
    stdb = np.std(countvalues2) #calculate standard deviation
    cut_upper = meanb+5.*stdb
    cut_lower = meanb-5.*stdb
    clippedvalues = countvalues2[(countvalues2>=cut_lower) & (countvalues2<=cut_upper)]
    n_photons = np.mean(clippedvalues)
    sigma = np.sqrt(n_photons)
    std = np.std(clippedvalues)
    '''
    n_photons = np.mean(boxflatten)
    sigma = np.sqrt(n_photons)
    std = np.std(boxflatten)
    gain = (sigma/std)**2 #calculate gain
    print 'mean = ', n_photons
    print 'sigma = ', sigma
    print 'std = ', std
    print 'calculated gain = ', gain
    head_gain = header2["EGAIN"] #get gain from header
    print 'gain in header = ', head_gain

    plt.show()

#masterflat(jasminepath)
gain(jasminepath)
