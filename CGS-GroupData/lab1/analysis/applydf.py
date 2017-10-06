import numpy as np
from astropy.io import fits
import os
import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore',category=AstropyWarning)

#test change

lorenapath = "/home/lmezini/lab1"
lorenanewpath = "/home/lmezini/lab1/calibrated"
jasminepath = '/home/jgarani/AST443/CGS-GroupData/lab1/raw-data/'
jasminenewpath = '/home/jgarani/AST443/CGS-GroupData/lab1/calibration/'

#testing testing 123

path = jasminepath
newpath = jasminenewpath

def applydf(path,newpath):
    all_files = []
    dark_hdulist = fits.open("master_dark.fits")
    dark_data = dark_hdulist[0].data
    flat_hdulist = fits.open("master_flat.fits")
    flat_data = flat_hdulist[0].data
    
    #list with bad files
    badfiles = ['L1-sci.00000063.FIT','L1-sci.00000094.FIT','L1-sci.00000197.FIT','L1-sci.00000537.FIT','L1-sci.00000550.FIT','L1-sci.00000551.FIT','L1-sci.00000552.FIT','L1-sci.00000553.FIT','L1-sci.00000554.FIT','L1-sci.00000555.FIT','L1-sci.00000556.FIT','L1-sci.00000557.FIT','L1-sci.00000558.FIT','L1-sci.00000559.FIT','L1-sci.00000560.FIT','L1-sci.00000565.FIT']
    
    for f in os.listdir(path):
        if "sci" in f and f not in badfiles:
            print f
            hdulist = fits.open(path + '/' + f, ignore_missing_end=True)
            header = hdulist[0].header
            imagedata = hdulist[0].data
            df_sci = (imagedata.flatten()-dark_data.flatten())/flat_data.flatten()
            newhdu = fits.PrimaryHDU(df_sci)
            newhdu.writeto(newpath+'/df-'+f,overwrite=True)
    
applydf(path,newpath)
