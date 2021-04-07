from pathlib import Path
from numpy import loadtxt

from copernicus_search import copernicus_search

userDataPath = Path().resolve() / '..' / 'userdata'
staticDataPath = Path(str(loadtxt(userDataPath / 'staticDataPath.txt', dtype='str')))
import sys
sys.path.insert(0, str(staticDataPath))
import values

numberOfResults = 10
filterTagName = 'sentinel3:cloudypixels'
filterAttribute = 'percentage'
filterMin = 0
filterMax = 10
filterDateRange = '2018-06-01T00:00:00.000Z TO NOW'

def search_for_cloudy():

    urls = copernicus_search(numberOfResults, filterTagName, filterAttribute, filterMin, filterMax, filterDateRange)

search_for_cloudy()