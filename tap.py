from urllib.request import urlopen
import pandas as pd
import json
import requests

BASE_VIZ = """http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync?\
request=doQuery&lang=adql&format=json&query=""".replace(' ','')

TABLE = 'I/355/gaiadr3'

sel_cols = ['Source','RAJ2000','DEJ2000', #'RandomI',
            'Plx','Dist','PM','pmRA','pmDE','RV','Teff','nueff','"[Fe/H]"','logg',
            'Gmag','BPmag','RPmag','FG','FBP','FRP',
            'HIP','SDSS13',
            #FLAGS:
            'XPcont','XPsamp','RVS','EpochPh','EpochRV']


def get(script):
    script = ' '.join(script.strip().split('\n'))
    url = BASE_VIZ+script.replace(' ', '%20')
    dc = json.loads(urlopen(url).read().decode('utf-8'))
    return dc


def columns(table=TABLE, ucd=False):
    ucd = ', ucd' if ucd else ''
    cols = 'column_name, description, unit' + ucd
    script = f"SELECT {cols} FROM tap_schema.columns WHERE table_name='{table}'"
    r = get(script)
    cols = [i['name'] for i in r['metadata']]
    df = pd.DataFrame(r['data'], columns=cols)
    return df.set_index('column_name')


def sql2df(script):
    r = get(script)
    cols = [i['name'] for i in r['metadata']]
    data = pd.DataFrame(r['data'], columns=cols)
    meta = pd.DataFrame(r['metadata'])
    meta = meta[['name', 'description', 'unit']].set_index('name')
    return data, meta

#cols = columns("I/355/gaiadr3")
cols = ','.join(sel_cols)
script = f'SELECT {cols} FROM "I/355/gaiadr3" WHERE source=3602681622301019520'
df, meta = sql2df(script)

"""
Source     3602681622301019520
RAJ2000             179.182691
DEJ2000              -1.143832
Plx                     2.6001
Dist                  324.2251
PM                      42.405
pmRA                    -41.84
pmDE                    -6.902
RV                        None
Teff                    3970.9
nueff                    1.339
[Fe/H]                  0.1278
logg                    4.6669
Gmag                 15.959896
BPmag                16.995348
RPmag                14.951092
FG                   7780.1558
FBP                2174.090801
FRP                 8293.19102
HIP                       None
SDSS13     1237674648854593669
XPcont                       1
XPsamp                       0
RVS                          0
EpochPh                      0
EpochRV                      0
"""
