from urllib.request import urlopen
import cgi


def get_filename(url):
    r = urlopen(url)
    msg = r.info()['Content-Disposition']
    value, params = cgi.parse_header(msg)
    filename = params["filename"]
    return filename



##BASE = 'https://gea.esac.esa.int/data-server/data?RETRIEVAL_TYPE='
##
##source_id = 30343944744320
##
##url = BASE + f'ALL&ID={source_id}&' + \
##      'DATA_STRUCTURE=INDIVIDUAL&RELEASE=Gaia+DR3&FORMAT=csv'
##
##urlretrieve(url, get_filename(url))

