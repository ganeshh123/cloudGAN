import sys
import requests
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('..').resolve() / '.env'

def authenticated_session():

    # Load Authentication Environment Variables
    load_dotenv()

    if os.getenv('copernicus_username') == None:
        print('\n\nField "copernicus_username" missing in ' + str(env_path) + ' file\n\n')
        return
    
    if os.getenv('copernicus_pass') == None:
        print('\n\nField "copernicus_pass" missing in ' + str(env_path) + ' file\n\n')
        return
    
    # create a session authenticated with our Copernicus credentials
    session = requests.Session()
    session.auth = (os.getenv('copernicus_username'), os.getenv('copernicus_pass'))

    testResponse = session.get('https://scihub.copernicus.eu/dhus/search?start=0&rows=100&q=(platformname:Sentinel-3 AND filename:S3A* AND producttype:SL_1_RBT___ AND ingestiondate:[2020-06-01T00:00:00.000Z TO NOW])')
    if testResponse.status_code == 401:
        print('\n\nCopernicus Credentials are Invalid')
        print('Please fill in the "copernicus_username" and "copernicus_password" fields correctly in the .env file!\n\n')
        return

    return session