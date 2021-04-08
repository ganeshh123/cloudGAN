import sys
#https://stackoverflow.com/questions/5953373/how-to-split-image-into-multiple-pieces-in-python/62013714#62013714
from PIL import Image as PillowImage
from pathlib import Path
import os

generatedFileNum = 0

def slice_image(input, xPieces, yPieces, outputPath):
    fileNameBits = Path(input).stem.split('-')
    print(fileNameBits)
    try:
        fileNum = int(fileNameBits[0])
        filename = fileNameBits[1]
    except:
        fileNum = generatedFileNum
        generatedFileNum = generatedFileNum + 1
        filename = fileNameBits[0]
    
    im = PillowImage.open(input)
    imgwidth, imgheight = im.size
    height = imgheight // yPieces
    width = imgwidth // xPieces
    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            a = im.crop(box)
            try:
                tileFileName = str(fileNum) + '-' + str(i+1) + '-' + str(j+1) + '-' + str(filename) + '-'+ '.jpg'
                tileOutputPath = Path.resolve(outputPath) / tileFileName
                a.save(tileOutputPath)
            except:
                print('Error saving tile')