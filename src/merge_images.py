import sys
import numpy as np
from pathlib import Path
from PIL import Image as PillowImage
from skimage.exposure import exposure

def merge_images(landscapePath, cloudPath):
	landscape = PillowImage.open(landscapePath)
	clouds = PillowImage.open(cloudPath)
	output = PillowImage.blend(landscape, clouds, 0.5)

	output = output.convert('RGB')
	output = exposure.rescale_intensity(output, out_range=(0, 255))
	output = PillowImage.fromarray(np.uint8(output))

	return output