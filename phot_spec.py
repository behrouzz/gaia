import pandas as pd
from hypatie.time import jd_to_datetime

file = 'data/data01\\EPOCH_PHOTOMETRY-Gaia DR3 30343944744320.csv'

def ep_phot(file, to_datetime=False):
    """
    light curves in bands G, BP and RP

    flux : integrated flux value of transit [e− s−1]
    flux_error : uncertainty on flux [e− s−1]
    mag : Vega magnitude in associated band [mag]

    has_epoch_photometry = 't'
    """
    df = pd.read_csv(file)
    df = df[df['rejected_by_photometry']==False]
    if to_datetime:
        df['TCB'] = [jd_to_datetime(i+2455197.5) for i in df['time']]
        df.set_index('TCB', inplace=True)
        cols = ['mag', 'flux', 'flux_error']
    else:
        cols = ['time', 'mag', 'flux', 'flux_error']
    g = df.loc[df['band']=='G', cols]
    b = df.loc[df['band']=='BP', cols]
    r = df.loc[df['band']=='RP', cols]
    return g, b, r


#g, b, r = ep_phot(file, to_datetime=True)

#============================================================

file = 'data/data01\\XP_SAMPLED-Gaia DR3 30343944744320.csv'

def xp_samp(file):
    """
    Wavelength: nm
    Flux: Externally-calibrated combined BP and RP flux. [W / (m2 nm)]

    BP/RP externally calibrated sampled mean spectrum. All mean spectra
    are sampled to the same set of absolute wavelength positions,
    viz. 343 values from 336 to 1020 nm with a step of 2 nm.

    has_xp_sampled = 't'
    """
    cols = ['wavelength', 'flux', 'flux_error']
    return pd.read_csv(file, usecols=cols)

#df = xp_samp(file)

#============================================================

file = 'data/data01\\RVS-Gaia DR3 30343944744320.csv'

def rvs(file):
    """
    Wavelength: 846 to 870
    Flux: ?

    The spectra are in the rest frame, they are normalised and their
    wavelength grid ranges from 846 to 870 nm in steps of 0.01 nm (2401
    elements).

    has_rvs = 't'
    """
    cols = ['wavelength', 'flux', 'flux_error']
    return pd.read_csv(file, usecols=cols)

#df = rvs(file)

#============================================================
"""
https://gaiaxpy.readthedocs.io/en/latest/description.html#general-description

1) internally calibrated spectra : electrons per second per pixel sample
2) external or absolute system : W nm-1 m-2
"""

file = 'data/data01\\XP_CONTINUOUS-Gaia DR3 30343944744320.csv'

# if gaiaxpy & astropy installed:
import numpy as np
from gaiaxpy import calibrate

def xp_cont(file, sampling=None, save_file=False):
    """
    mean BP and RP spectra based on the continuous representation in
    basis functions

    Wavelength: nm
    Flux: W / (m2 nm)

    has_xp_continuous = 't'
    """
    
    calibrated_df, sampling = calibrate(
        file, sampling=sampling, save_file=save_file)
    
    df = pd.DataFrame({'wavelength': sampling,
                       'flux': calibrated_df.iloc[0]['flux'],
                       'flux_error': calibrated_df.iloc[0]['flux_error']})
    return df
                             

#df = xp_cont(file, sampling=np.linspace(400, 900, 600))


