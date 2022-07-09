from astropy.io import fits

hdul = fits.open('data/data01.fits')
hdul.info()
hdul.close()
