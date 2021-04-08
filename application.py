import sys
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

userDataFolder = Path(sys.path[0]).resolve() / 'userdata'
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
staticDataPath.write(str(Path(sys.path[0]).resolve() / 'data'))
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
outputFolder = Path(sys.path[0]).resolve() / 'output'
outputFolder.mkdir(exist_ok=True)
(outputFolder / 'surface').mkdir(exist_ok=True)
(outputFolder / 'masks').mkdir(exist_ok=True)
(outputFolder / 'clouds').mkdir(exist_ok=True)
(outputFolder / 'images').mkdir(exist_ok=True)

print('Unzipping Cloudless Set...')
zipfile.ZipFile(Path(sys.path[0]).resolve() / 'data'/ 'surface_set.zip').extractall((outputFolder / 'surface').resolve())

print('Done')

print('\n\n------------------------------------------------------')

print('STEP 3 : Getting Cloudy Products\n\n')

print('Would you like to download new products?')
noValidDownloadInput = True
while(noValidDownloadInput):
    userWantsToDownload = input('y or n :')
    if userWantsToDownload == 'y':
        noValidDownloadInput = False

        print('How many products to download?')
        print(' Each product equals roughly 75 clouds')
        noValidProductNumberInput = True
        while(noValidProductNumberInput):
            requestedProductNumberInput = input('Number of products to download (between 1 and 50) : ')
            if requestedProductNumberInput.isdigit() and int(requestedProductNumberInput) >= 1 and int(requestedProductNumberInput) <= 50:
                requestedProductNumber = int(requestedProductNumberInput)
                print(requestedProductNumber, ' products to be downloaded...\n\n')
                noValidProductNumberInput = False
                os.system('python src/search_for_cloudy.py --productCount ' + str(requestedProductNumber))
                os.system('python src/copernicus_download.py')
            else:
                print('\n Invalid Input, please try again!')

    elif userWantsToDownload == 'n':
        print('No products will be downloaded')
        print('Please put your own product zip files in userdata/product_store folder')
        noValidDownloadInput = False
    else:
        print('\n Invalid Input, please try again!')

try:
    os.remove(userDataFolder / 'imagePaths.txt')
except:
    print('nada')

os.system('python src/unzip_images.py')
print('Done')

print('\n\n------------------------------------------------------')

print('STEP 5 : Processing Inputs \n\n')

print('\nConverting to RGB Images\n')
os.system('python src/build_rgb_images.py')
print('\nExtracting Masks\n')
os.system('python src/build_mask_images.py')
print('\nSlicing into Tiles\n')
os.system('python src/slice_images.py')
print('\nSorting by Cloud Cover\n')
os.system('python src/sort_tiles.py')
print('\nPreparing CycleGAN\n')
os.system('python src/prep_cyclegan.py')
print('\nDone\n')

print('\n\n------------------------------------------------------')

print('STEP 6 : Building Fake Clouds \n\n')

print('\n Running CycleGAN\n')
os.system('python src/run_cyclegan.py')
print('\n Fetching Clouds\n')
os.system('python src/finish_cyclegan.py')
print('\nDone\n')

print('\n\n------------------------------------------------------')

print('STEP 7 : Overlaying Clouds \n\n')

print('\n Overlaying Clouds\n')
os.system('python src/overlay_clouds.py')
print('\nDone\n')
print('\nFinished - Generated Training Set can be found in outputs folder!\n')