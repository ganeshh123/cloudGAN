import numpy as np
from count_nonblack import count_nonblack
from PIL import Image as PillowImage

def percentage_cloud(imageFile):
    img = PillowImage.open(imageFile)
    resolution = img.size[0] * img.size[1]
    nonblack = count_nonblack(img)
    percentage = nonblack / resolution
    return percentage