# https://www.cosmos.esa.int/web/gaia-users/archive/programmatic-access#CommandLine_DataLink

from urllib.request import urlopen, urlretrieve
import pandas as pd
import json, os
from zipfile import ZipFile
from glob import glob




BASE = 'https://gea.esac.esa.int/data-server/data?RETRIEVAL_TYPE='

VALID_RT = ['EPOCH_PHOTOMETRY', 'XP_SAMPLED', 'XP_CONTINUOUS',
             'MCMC_GSPPHOT', 'MCMC_MSC',  'RVS', 'ALL']

VALID_DS = ['INDIVIDUAL','COMBINED','RAW']

class DataLink:
    """
    Gaia DataLink class

    

    ARGUMENTS:
    ----------
    source_id (int or list): object or objects source_id(s)
    retrieval_type (str): 'EPOCH_PHOTOMETRY', 'XP_SAMPLED', 'XP_CONTINUOUS',
                          'MCMC_GSPPHOT', 'MCMC_MSC',  'RVS', 'ALL'
                          (Default: 'ALL')
    data_structure (str): 'INDIVIDUAL','COMBINED','RAW'
                          (Default: 'INDIVIDUAL')
    
    ATTRIBUTES:
    -----------
    multi (bool) : if the request is for multiple souces
    url (str) : the url of the file to download

    METHODS:
    --------
    datalink_url : return url of the file to download
    download : download the requested file

    Ref: https://www.cosmos.esa.int/web/gaia-users/archive/programmatic-access
    """
    def __init__(self, source_id, retrieval_type=None, data_structure=None):
        self.multi = False
        self.source_id = self.__check_source_id(source_id)
        self.retrieval_type = self.__check_retrieval_type(retrieval_type)
        self.data_structure = self.__check_data_structure(data_structure)
        self.url = self.datalink_url()
        
        
    def __check_source_id(self, source_id):
        if isinstance(source_id, list):
            self.multi = True
            source_id = [str(i) for i in source_id]
            source_id = ','.join(source_id).replace(' ', '')
        return source_id

    def __check_retrieval_type(self, retrieval_type):
        if retrieval_type is None:
            retrieval_type = 'ALL'
        elif retrieval_type not in VALID_RT:
            raise Exception(f'retrieval_type not valid! Options::\n{VALID_RT}')
        return retrieval_type

    def __check_data_structure(self, data_structure):
        if data_structure is None:
            data_structure = 'INDIVIDUAL'
        elif data_structure not in VALID_DS:
            raise Exception(f'data_structure not valid! Options::\n{VALID_DS}')
        return data_structure


    def datalink_url(self):
        #format='fits' to be added
        url = BASE + f'{self.retrieval_type}&ID={self.source_id}&' + \
              f'DATA_STRUCTURE={self.data_structure}&RELEASE=Gaia+DR3&FORMAT=fits'
        return url


    def download(self, filename=None):

        if self.multi or self.retrieval_type=='ALL':
            ext = '.zip'
        else:
            ext = '.fits'

        if not os.path.isdir('data'):
            os.makedirs('data')
            
        if filename is None:
            i = 1
            while True:
                if os.path.exists('data/data'+str(i).zfill(2)+ext):
                    i = i + 1
                else:
                    filename = 'data/data'+str(i).zfill(2)+ext
                    break
        
        self.filename = filename
        urlretrieve(self.url, filename)


    def extract(self, folder='data'):
        
        if self.filename[-4:]=='.zip':
            with ZipFile(self.filename, 'r') as zip:
                zip.extractall(folder)
            self.files = [i for i in glob(folder+'/*') if i[-4:]!='.zip']
        else:
            print('Not a zip file!')

