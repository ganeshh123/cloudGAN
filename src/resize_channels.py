from image import ImageLoader
from skimage.transform import resize
import numpy as np

def resize(path):
    loader = ImageLoader(path)
    bts=loader_load.bts()
    bt_channels = bts.to_array().values
    bt_resized = resize(bt_channels, (bt_channels.shape[0], bt_channels.shape[1] // 4, bt_channels.shape[2] // 4), anti_aliasing=True)
    return bt_resized