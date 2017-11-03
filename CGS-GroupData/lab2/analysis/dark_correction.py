#Jasmine Garani, Lorena Mezini, Patrick Payne
#Created 10/21/17
#Purpose: For lab2, correct science images and flats using the darks of appropriate exopusure time
#================================================================

import numpy as np
from astropy.io import fits
import os

#================================================================

jasminepath = "/home/jgarani/AST443/CGS-GroupData/lab2/usedata/"
jasmineoutpath = "/home/jgarani/AST443/CGS-GroupData/lab2/afterdark/"
path = jasminepath #path where data is
outpath = jasmineoutpath #path to output new files


#Corrects neon science files, exposure time of 1200s
def neon_dark(path,outpath):
    all_dark1200 = [] #make empty array for darks
    for f in os.listdir(path):
        if 'dark' in f and 'neon' in f: #find only darks with correct exposure time
            print f
            darkhdulist1200 = fits.open(path + '/' + f) #open darks
            darkdata1200 = darkhdulist1200[0].data
            all_dark1200.append(darkdata1200)
    masterdark1200 = np.median(all_dark1200,axis=0) #make master dark
    for s in os.listdir(path):
        if 'sci-neon' in s or 'star-neon' in s or 'arc-neon' in s: #get science files
            print s
            scineonhdulist = fits.open(path + '/' + s)
            scineon = scineonhdulist[0].data
            d_scineon = scineon - masterdark1200 #subtract dark
            newscineonhdu = fits.PrimaryHDU(d_scineon)
            s = s.replace('.FIT','.fits')
            newscineonhdu.writeto(outpath + '/' + 'd-' + s,overwrite=True) #write out new file

#Corrects hg science files, exposure time of 240s
def hg_dark(path,outpath):
    all_dark240 = [] #make empty array for darks
    for f in os.listdir(path):
        if 'dark' in f and 'hg' in f: #find only darks with correct exposure time
            print f
            darkhdulist240 = fits.open(path + '/' + f) #open darks
            darkdata240 = darkhdulist240[0].data
            all_dark240.append(darkdata240)
    masterdark240 = np.mean(all_dark240,axis=0) #make master dark
    for s in os.listdir(path):
        if 'sci-hg' in s or 'star-hg' in s or 'arc-hg' in s: #get science files
            print s
            scihghdulist = fits.open(path + '/' + s)
            scihg = scihghdulist[0].data
            d_scihg = scihg - masterdark240 #subtract dark
            newscihghdu = fits.PrimaryHDU(d_scihg)
            s = s.replace('.FIT','.fits')
            newscihghdu.writeto(outpath + '/' + 'd-' + s,overwrite=True) #write out new file

#Corrects flat files, exposure time of 360s
def flat_dark(path,outpath):
    all_dark360 = [] #make empty array for darks
    for f in os.listdir(path):
        if 'dark' in f and 'flat' in f: #find only darks with correct exposure time
            print 'f = ', f
            darkhdulist360 = fits.open(path + '/' + f) #open darks
            darkdata360 = darkhdulist360[0].data
            all_dark360.append(darkdata360)
    masterdark360 = np.mean(all_dark360,axis=0) #make master dark
    for s in os.listdir(path):
        if 'flat' in s and 'hg' in s: #get flat files
            print 's = ', s
            darkflathdulist = fits.open(path + '/' + s)
            darkflat = darkflathdulist[0].data
            d_darkflat = darkflat - masterdark360 #subtract dark
            newdarkflathdu = fits.PrimaryHDU(d_darkflat)
            s = s.replace('.FIT','.fits')
            newdarkflathdu.writeto(outpath + '/' + 'd-' + s,overwrite=True) #write out new file

neon_dark(path,outpath)
hg_dark(path,outpath)
#flat_dark(path,outpath)
