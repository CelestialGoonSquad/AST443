import numpy as np
from astropy.io import fits
import os
import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore',category=AstropyWarning)

path = "/home/lmezini/lab1"
newpath = "/home/lmezini/lab1/calibrated"

def applydf(path,newpath):
    all_files = []
    dark_hdulist = fits.open("master_dark.fits")
    dark_data = dark_hdulist[0].data
    flat_hdulist = fits.open("master_flat.fits")
    flat_data = flat_hdulist[0].data
    for f in os.listdir(path):
        if "sci" in f:
            print f
            hdulist = fits.open(path + '/' + f, ignore_missing_end=True)
            header = hdulist[0].header
            imagedata = hdulist[0].data
            df_sci = (imagedata.flatten()-dark_data.flatten())/flat_data.flatten()
            newhdu = fits.PrimaryHDU(df_sci)
            newhdu.writeto(newpath+'/df-'+f,clobber=True)
    
applydf(path,newpath)
