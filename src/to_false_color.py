import sys
import matplotlib.pyplot as plt
from pathlib import Path, PurePath
from image import ImageLoader, Regrid
from skimage.transform import resize
from skimage.exposure import exposure
import numpy as np
import sys
from PIL import Image as PillowImage
from PIL import ImageEnhance
import skimage

def to_false_color(imagePath):
    path = imagePath
    print('---')
    product = ImageLoader(path)
    # Get Channels
    s1 = product.load_reflectance_channel(path, 1, 'an').to_array().values[0]
    s3 = product.load_reflectance_channel(path, 3, 'an').to_array().values[0]
    s5 = product.load_reflectance_channel(path, 5, 'an').to_array().values[0]

    # Deal with NaNs
    s1 = np.where(np.isnan(s1), 0, s1)
    s3 = np.where(np.isnan(s3), 0, s3)
    s5 = np.where(np.isnan(s5), 0, s5)

    # Clip pixels > 1 to 1. This keeps the image in the range 0-1
    s1 = np.where(s1 > 1., 1., s1)
    s3 = np.where(s3 > 1., 1., s3)
    s5 = np.where(s5 > 1., 1., s5)

    #plt.hist(s1.flatten(), bins=100)
    #plt.show()


    # Construct Image
    img = np.zeros((s1.shape[0], s1.shape[1], 3))
    img[..., 0] = np.minimum(1, (s3 + s5) / 2)
    img[..., 1] = np.minimum(1, s3)
    img[..., 2] = np.minimum(1, (s3 + s1) / 2)

    #Produce Image
    img = skimage.exposure.rescale_intensity(img, out_range=(0, 255))

    rgbImage = PillowImage.fromarray(np.uint8(img))
    return rgbImage