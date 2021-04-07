from PIL import Image as PillowImage
from PIL import ImageEnhance as PillowEnhance
from pathlib import Path

def merge_images(landscapePath, cloudPath):
    landscape = PillowImage.open(landscapePath).convert("RGBA")
    clouds = PillowImage.open(cloudPath).convert("RGBA")
    output = PillowImage.blend(landscape, clouds, 0.5)

    brightnessEnhancement = PillowEnhance.Brightness(output)
    output = brightnessEnhancement.enhance(1.75)

    colorBoost = PillowEnhance.Color(output)
    output = colorBoost.enhance(1.25)

    output = output.convert('RGB')

    return output