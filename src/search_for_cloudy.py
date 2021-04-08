import sys
from pathlib import Path
from numpy import loadtxt
import argparse

from copernicus_search import copernicus_search

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
staticDataPath = Path(str(loadtxt(userDataPath / 'staticDataPath.txt', dtype='str')))
sys.path.insert(0, str(staticDataPath))
import values

numberOfResults = 20
filterTagName = 'sentinel3:cloudypixels'
filterAttribute = 'percentage'
filterMin = 50
filterMax = 100
filterDateRange = '2018-06-01T00:00:00.000Z TO NOW'

def search_for_cloudy(resultCount=numberOfResults):

    urls = copernicus_search(resultCount, filterTagName, filterAttribute, filterMin, filterMax, filterDateRange)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--productCount', help='Number of SLSTR Products to Search For', type=int)
    arguments = parser.parse_args()


if(arguments.productCount):
    search_for_cloudy(arguments.productCount)
else:
    search_for_cloudy()