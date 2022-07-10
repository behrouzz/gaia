import pandas as pd
from datetime import timedelta

file = 'data/data01\\EPOCH_PHOTOMETRY-Gaia DR3 30343944744320.csv'

df = pd.read_csv(file)
df = df[df['rejected_by_photometry']==False]
cols = ['time', 'mag', 'flux', 'flux_error']


#df['time'] =
#Time(t+offset, format='jd', scale='tcb').to_datetime()

from hypatie.time import tdb2utc, jd_to_datetime


def time_to_utc(t):
    offset = 2455197.5
    jd = t + offset
    mjd = jd - 2400000.5
    dt = (1.55051976772e-8 * (mjd-43144) * 86400 + 6.55e-5)
    TCB = jd_to_datetime(jd)
    TDB = TCB - timedelta(seconds=dt)
    return tdb2utc(TDB)

def time_to_utc2(t):
    # https://syrte.obspm.fr/iauJD16/klioner.pdf
    offset = 2455197.5
    jd = t + offset

    T0 = 2443144.5003725
    Lb = 1.550519768 * 10**-8
    tdb0 = timedelta(seconds=-6.55e-5)
    TCB = jd_to_datetime(jd)
    TDB = TCB - Lb*(jd-T0)*86400 + tdb0
    return tdb2utc(TDB)

t = [time_to_utc2(i) for i in list(df['time'])]

g = df.loc[df['band']=='G', cols]
b = df.loc[df['band']=='BP', cols]
r = df.loc[df['band']=='RP', cols]

#=============================
from astropy.time import Time
offset = 2455197.5

t_ast = [Time(i+offset, format='jd', scale='tcb').to_datetime() for i in list(df['time'])]

for i in t:
    print(i)
