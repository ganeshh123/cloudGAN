import sys
from PIL import Image as PillowImage

def crop_image(image, left, top, right, bottom ):
    croppedTopLeftX = left
    croppedTopLeftY = top
    croppedBottomRightX = image.width - right
    croppedBottomRightY = image.height - bottom
    return image.crop((croppedTopLeftX, croppedTopLeftY, croppedBottomRightX, croppedBottomRightY))