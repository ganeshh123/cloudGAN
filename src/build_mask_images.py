import sys
from numpy import loadtxt
from pathlib import Path
from PIL import Image as PillowImage
from get_cloud_mask import get_cloud_mask
from to_cloud_mask_image import to_cloud_mask_image
from crop_image import crop_image

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
productStorePath = userDataPath / 'product_store'
outputMaskPath = userDataPath / 'mask_store'
imageListPath = userDataPath / 'imagePaths.txt'

def build_mask_images(imagePaths=loadtxt(imageListPath, dtype='str')):
    index = 1
    for imagePath in imagePaths:
        print(' >   Building Mask of ' + str(imagePath))

        # Build Mask Image
        maskImage = to_cloud_mask_image(get_cloud_mask(imagePath))
        # Crop Black Borders
        cropped = crop_image(maskImage, 100, 0, 100, 0)

        # Save to Mask Store
        imagePathFixed = str(imagePath).replace('.', '')[:-1]
        newImageName = str(index) + '-' + Path(imagePathFixed).stem + '.png'
        newImagePath = outputMaskPath / newImageName
        cropped.save(newImagePath)

        index = index + 1

build_mask_images()