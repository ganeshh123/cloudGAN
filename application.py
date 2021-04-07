import os
from pathlib import Path
import zipfile


print('\n\nCloud Masking Training Set Generator')

## Installing Requirements

print('\n\n------------------------------------------------------')

print('STEP 1 : Installing Requirements, please wait....\n\n')
os.system('python -m pip install -r src/requirements.txt')

print('\n\n------------------------------------------------------')

print('STEP 2 : Setting Up...\n\n')

print('Creating Files and Folders')

#Create env file
open('.env', 'a+').close()

userDataFolder = Path().resolve() / 'userdata'
# Create User Data Folder
userDataFolder.mkdir(exist_ok=True)
(userDataFolder / 'product_store').mkdir(exist_ok=True)
(userDataFolder / 'rgb_store').mkdir(exist_ok=True)
(userDataFolder / 'mask_store').mkdir(exist_ok=True)
(userDataFolder / 'cyclegan_input').mkdir(exist_ok=True)
(userDataFolder / 'cyclegan_output').mkdir(exist_ok=True)
(userDataFolder / 'cyclegan_output').mkdir(exist_ok=True)

# Absolute Path to Static Data
staticDataPath = open(userDataFolder / 'staticDataPath.txt' , 'w+')
staticDataPath.write(str(Path().resolve() / 'data'))
staticDataPath.close()
# Absolute Path to UserData
userDataPath = open(userDataFolder / 'userDataPath.txt' , 'w+')
userDataPath.write(str(userDataFolder.resolve()))
userDataPath.close()

# Create File to Store Parameters
open(userDataFolder / 'parameters.txt' , 'a+').close()
# Create File to Store Search Results for Download
open(userDataFolder / 'searchResults.txt' , 'a+').close()

# Create Output Directories
outputFolder = Path().resolve() / 'output'
outputFolder.mkdir(exist_ok=True)
(outputFolder / 'surface').mkdir(exist_ok=True)
(outputFolder / 'masks').mkdir(exist_ok=True)
(outputFolder / 'clouds').mkdir(exist_ok=True)
(outputFolder / 'images').mkdir(exist_ok=True)

print('Unzipping Cloudless Set...')
zipfile.ZipFile(Path().resolve() / 'data'/ 'surface_set.zip').extractall((outputFolder / 'surface').resolve())

print('\n\n------------------------------------------------------')



