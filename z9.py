from astropy.io import fits

hdul = fits.open('data/test/EPOCH_PHOTOMETRY-Gaia DR3 30343944744320.fits')
hdul.info()
hdul.close()
