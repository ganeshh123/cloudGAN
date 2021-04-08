import sys
from PIL import Image as PillowImage
from PIL import ImageEnhance
import skimage
import numpy as np
from pathlib import Path, PurePath

def to_cloud_mask_image(cloudMask):
    img = skimage.exposure.rescale_intensity(cloudMask.values, out_range=(0, 255))
    picture = PillowImage.fromarray(img.astype('uint8'), mode='L')
    doubled = picture.resize((3000, 2400))
    return doubled