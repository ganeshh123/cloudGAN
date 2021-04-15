import sys
from pathlib import Path
from merge_images import merge_images
import os

outputFolder = Path(sys.path[0]).resolve() / '..' / 'output'
defaultSurfaceFolder = (outputFolder / 'surface').resolve()
defaultMaskFolder = (outputFolder / 'masks').resolve()
defaultCloudFolder = (outputFolder / 'clouds').resolve()
defaultImageFolder = (outputFolder / 'images').resolve()

def overlay_clouds(surfaceFolder=defaultSurfaceFolder, cloudFolder=defaultCloudFolder, imageFolder=defaultImageFolder):

    surfaceImageCount = len(os.listdir(defaultSurfaceFolder))

    for cloudFileName in os.listdir(defaultCloudFolder):
        for surfaceFileName in os.listdir(defaultSurfaceFolder):

            surfaceIndex = str(int(cloudFileName[0:5]) % surfaceImageCount).zfill(5)

            if surfaceIndex == surfaceFileName[0:5]:
                cloudFilePath = str((cloudFolder / cloudFileName).resolve())
                surfaceFilePath = str((surfaceFolder / surfaceFileName).resolve())
                print('Overlaying Cloud... ' + cloudFileName + ' on ' + surfaceFileName)
                overlayImage = merge_images(surfaceFilePath, cloudFilePath)
                overlayImageName = cloudFileName[0:5] + '-image-' + cloudFileName[-102:]
                overlayImage.save(imageFolder / overlayImageName)
                print('>    Created ' + overlayImageName + ' successfully!')


overlay_clouds()