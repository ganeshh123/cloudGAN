import zipfile
import os
from pathlib import Path

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
productStorePath = userDataPath / 'product_store'

def unzip_images(directory=productStorePath):

    # Open File to write Image Folder Paths into
    resultsFile = open(userDataPath.resolve() / 'imagePaths.txt', 'a+')
    print(directory)

    zipFiles = []
    extractedPaths = []

    # Add any zip files in downloads folder to be extracted
    for file in os.listdir(directory):
        if file.endswith('.zip'):
            zipFilePath = os.path.join(directory, file)
            zipFiles.append(zipFilePath)

    index = 1
    for zipFilePath in zipFiles:
        # Extract each zip file
        print(' >   Extracting ' + str(zipFilePath))
        zipfile.ZipFile(zipFilePath).extractall(directory)
        extractedPath = zipfile.ZipFile(zipFilePath).namelist()[0]
        extractedPaths.append(extractedPath)
        print(str((productStorePath / extractedPath).resolve()),file=resultsFile)
            
    resultsFile.close()

    return extractedPaths

unzip_images()