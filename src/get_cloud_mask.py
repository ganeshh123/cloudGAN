from pathlib import Path, PurePath
from image import ImageLoader
from skimage.transform import resize
from skimage.exposure import exposure
import numpy as np
import sys
from PIL import Image as PillowImage
from PIL import ImageEnhance

def get_cloud_mask(imagePath):
    path = imagePath
    print('---')
    product = ImageLoader(path)
    flags = product.load_flags('in')
    return flags.bayes_in