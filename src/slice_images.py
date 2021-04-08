from pathlib import Path
import os
from slice_image import slice_image

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
defaultImagesPath = (userDataPath / 'rgb_store').resolve()
defaultMasksPath = (userDataPath / 'mask_store').resolve()

def slice_images(imagesPath=defaultImagesPath, masksPath=defaultMasksPath, extension='.jpg'):

    imageFiles = []
    maskFiles = []

    imageTilesPath = defaultImagesPath / 'tiles/'
    maskTilesPath = defaultMasksPath / 'tiles/'

    if not os.path.exists(imageTilesPath):
        os.makedirs(imageTilesPath)

    if not os.path.exists(maskTilesPath):
        os.makedirs(maskTilesPath)
    
    for file in os.listdir(imagesPath):
        if file.endswith(extension):
            imageFilePath = os.path.join(imagesPath, file)
            imageFiles.append(imageFilePath)

    for file in os.listdir(masksPath):
        if file.endswith(extension):
            maskFilePath = os.path.join(masksPath, file)
            maskFiles.append(maskFilePath)

    i = 0
    for i in range(len(imageFiles)):
        print(' >   Image: ', imageFiles[i])
        print('     >   Slicing Image....')
        slice_image(imageFiles[i], 14, 12,imageTilesPath)
        print('     >   Slicing Mask....')
        slice_image(maskFiles[i], 14, 12, maskTilesPath)

slice_images()