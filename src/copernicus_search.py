#!/usr/bin/env python
# coding: utf-8

#Returns an array of manifests and filters values within a specific range

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
import os

from authenticated_session import authenticated_session
from image_grayscale import image_grayscale

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'

def copernicus_search(amount, tagname, property, min, max, dateRange, footprint='none'):
    
    if footprint != 'none':
        print('\n\n\nQuery:', amount, 'results, where', tagname, property, 'is between', min, 'and', max, 'with a date range of ', dateRange, ' and in the area of ' + footprint)
    else:
        print('\n\n\nQuery:', amount, 'results, where', tagname, property, 'is between', min, 'and', max, 'with a date range of ', dateRange)

     # Authenticate Session with Copernicus
    print('\nCreating Authenticated Session ...')
    if authenticated_session() == None:
        print('Authentication Failure')
        return
    else:
        session = authenticated_session()

    results = []
    current = 0

    print('\nSearching....')

    while len(results) < amount:
        # Search for files via Copernicus API
        if footprint != 'none':
            url = 'https://scihub.copernicus.eu/dhus/search?start='+ str(current) + '&rows=100&q=(platformname:Sentinel-3 AND filename:S3A* AND producttype:SL_1_RBT___ AND ingestiondate:[' + dateRange + '] AND footprint:' + footprint + ')'
        else:
            url = 'https://scihub.copernicus.eu/dhus/search?start='+ str(current) + '&rows=100&q=(platformname:Sentinel-3 AND filename:S3A* AND producttype:SL_1_RBT___ AND ingestiondate:[' + dateRange + '])'

        print(url)
        response = session.get(url)

        if response.status_code == 200:
            # Parse the response with Beautiful Soup so we can search the XML
            xml = BeautifulSoup(response.text, features="lxml")

            print('Checking page', current, '...')
            print(' ->', url)
            # Find all entries returned by our search2
            entries = xml.find_all('entry')

            row = 0
            for entry in entries:

                # Build the URL of the manifest file for this product
                product_url = entry.find_all('link')[1]['href']
                filename = entry.find('str', {'name': 'filename'}).text
                manifest_url = f"{product_url}/Nodes('{filename}')/Nodes('xfdumanifest.xml')/$value"
                # Get the manifest file
                manifest = session.get(manifest_url, timeout=30)
                manifest = BeautifulSoup(manifest.text, features="lxml")
                value = float(manifest.find(tagname)[property])
                #print(current, tagname, property, value)
                print(' >>', row, ':', value)
                if(value >= min and value <= max):
                    print(' >   Potential Match Found : ', product_url, property, value)
                    previewUrl = f"{product_url}Products('Quicklook')/$value"
                    print(' >   Downloading Preview', previewUrl)
                    raw = session.get(previewUrl, timeout=30, allow_redirects=True)
                    open(userDataPath / 'preview.jpg', 'wb').write(raw.content)
                    print(' >   Checking if image is daytime...')
                    if not image_grayscale(userDataPath / 'preview.jpg'):
                        results.append(product_url)
                        print(' >   Added to download list')
                        print(amount - len(results), ' remaining')
                    else:
                        print(' >   Night time image, so skipped.')
                row = row + 1
                if(len(results) >= amount):
                    break
        
        else:
            print('Error!')
            print(response.text)
            
        current = current + 100

    #Dump Results in a file
    with open(userDataPath / 'searchResults.txt', 'a+') as resultsFile:
        for result in results:
            print(result,file=resultsFile)

    return results

#output = copernicus_search(10, 'sentinel3:cloudypixels', 'percentage', 20, 0)      
#print(output)     
