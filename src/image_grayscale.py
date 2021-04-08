import sys
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

default_image_path = Path('..').resolve() / 'training_data_generator/data_store/preview.jpg'

def image_grayscale(imagePath=default_image_path):
    imageObject = io.imread(imagePath)
    return np.all((imageObject[..., 0] == imageObject[..., 1]) & (imageObject[..., 1] == imageObject[..., 2]))