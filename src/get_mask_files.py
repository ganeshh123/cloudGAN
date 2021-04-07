from pathlib import Path
import os

userDataPath = Path().resolve() / '..' / 'userdata'
defaultMaskTilesPath = (userDataPath / 'mask_store' / 'tiles').resolve()
defaultImageFormat = '.jpg'

def get_mask_files(maskTilesPath=defaultMaskTilesPath, imageFormat=defaultImageFormat):

    maskFiles = []
    for file in os.listdir(maskTilesPath):
        if file.endswith(imageFormat):
            maskFilePath = os.path.join(maskTilesPath, file)
            maskFiles.append(maskFilePath)

    return maskFiles
