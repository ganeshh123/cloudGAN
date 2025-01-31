# Package Import
import sys
from numpy import loadtxt
from pathlib import Path
from PIL import Image as PillowImage
# Function Import
from to_false_color import to_false_color
from crop_image import crop_image

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
productStorePath = userDataPath / 'product_store'
outputImagePath = userDataPath / 'rgb_store'
imageListPath = userDataPath / 'imagePaths.txt'


def build_rgb_images(imagePaths=loadtxt(imageListPath, dtype='str', ndmin=1)):
    index = 1
    for imagePath in imagePaths:
        print(' >   Building Image of ' + str(imagePath))

        # Combine channels to build RGB image
        rgbImage = to_false_color(imagePath)
        # Crop black borders
        cropped = crop_image(rgbImage, 100, 0, 100, 0)

        # Save Image to RGB store
        imagePathFixed = str(imagePath).replace('.', '')[:-1]
        newImageName = str(index) + '-' + Path(imagePathFixed).stem + '.png'
        print(newImageName)
        newImagePath = outputImagePath / newImageName
        cropped.save(newImagePath)
        
        index = index + 1

build_rgb_images()