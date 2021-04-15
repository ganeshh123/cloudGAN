import sys
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
from numpy import loadtxt
import os
import shutil

from authenticated_session import authenticated_session

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
env_path = Path('..') / '.env'

# List of product URLS to download
searchResultsPath = userDataPath / 'searchResults.txt'
# Directory to store downloads
productStorePath = userDataPath / 'product_store'

def copernicus_download(urls=loadtxt(searchResultsPath, dtype='str', ndmin=1)):

    # Print the number of images to download
    print('To Download : ')
    print(' ' + str(urls.size) + ' images')

    # Authenticate Session with Copernicus
    print('Creating Authenticated Session ...')
    if authenticated_session() == None:
        print('Authentication Failure')
        return
    else:
        session = authenticated_session()

    print('Downloading...')
    print(type(urls))

    index = 1
    for url in urls:
        if os.path.exists(str(Path(str(productStorePath) + '/' + str(index) + '.zip').resolve())):
            # Skip if already downloaded
            print('Already downloaded  ' + url)
        else:
            download_link = url + '$value'
            print(' >>  ', index, download_link)
            with session.get(download_link, allow_redirects=True, stream=True) as r:
                if r.status_code != 200 :
                    # Print error message
                    print('Error!')
                    print(r.text)
                else:
                    #Write content to zip file
                    print('Downloading ...')
                    with open(str(productStorePath) + '/' + str(index) + '.zip', 'wb') as f:
                        shutil.copyfileobj(r.raw, f, length=16*1024*1024)
                
        
        index = index + 1
    
    print('\nDownloads Completed\n')

copernicus_download()