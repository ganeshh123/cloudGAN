import os
from percentage_cloud import percentage_cloud
from pathlib import Path
from shutil import copyfile
from get_mask_files import get_mask_files

userDataPath = Path().resolve() / '..' / 'userdata'
defaultImagesPath = (userDataPath / 'rgb_store').resolve()
defaultMasksOutputPath = (userDataPath / 'mask_store').resolve()

intervals = [0, 10, 99, 100]

def sort_tiles(maskFiles=get_mask_files(), imagesPath=defaultImagesPath, masksOutputPath=defaultMasksOutputPath, imagesOutputPath=defaultImagesPath, inputImageFilePath=defaultImagesPath):

    for inteval in intervals:
        folder = 'percentage' + str(inteval)
        intervalPathMask = masksOutputPath / folder
        if not os.path.exists(intervalPathMask):
            os.makedirs(intervalPathMask)
        intervalPathImage = imagesOutputPath / folder
        if not os.path.exists(intervalPathImage):
            os.makedirs(intervalPathImage)

    print('\nSorting...\n')
    for maskFile in maskFiles:
        percentageCloud = percentage_cloud(maskFile) * 100
        for inteval in intervals:
            if percentageCloud <= inteval:
                folder = 'percentage' + str(inteval)
                baseFileName = Path(maskFile).stem
                print('Sorting ...      ' + baseFileName)
                #Copy Mask
                outputMaskFileName = baseFileName + '____mask.jpg'
                outputMaskFilePath = masksOutputPath / folder / outputMaskFileName
                copyfile(maskFile, outputMaskFilePath)
                #Copy Associated Image
                imageFileName = baseFileName + '.jpg'
                imageFile = inputImageFilePath / 'tiles' / imageFileName
                if os.path.exists(imageFile):
                    outputImageFileName = baseFileName + '____image.jpg'
                    outputImageFilePath = imagesOutputPath / folder / outputImageFileName
                    copyfile(imageFile, outputImageFilePath)
                else:
                    print('>    ERROR')
                    print('         No Image found for mask:')
                    print('         ' + maskFile)
                break

sort_tiles()
