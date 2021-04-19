import sys
import os
from pathlib import Path
import shutil

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
resultsFolder = (userDataPath / 'cyclegan_output' / 'mask-cloud-networks' / 'test_latest' / 'images').resolve()
outputFolder = Path(sys.path[0]).resolve() / '..' / 'output'
maskOutput = (outputFolder / 'masks').resolve()
cloudOutput = (outputFolder / 'clouds').resolve()

def finish_cyclegan():

    masks = []
    clouds = []

    print('\n\nRetrieving CycleGAN Results\n')

    for filename in os.listdir(resultsFolder):
        if '_real_B' in filename:
            masks.append(filename)
        if 'fake_A' in filename:
            clouds.append(filename)

    index = 1
    for maskFileName in masks:
        indexString = str(index).zfill(5)
        identifierString = maskFileName.split('S')[0]
        cloudFileName = next(cloudFileName for cloudFileName in clouds if cloudFileName.split('S')[0] == identifierString)
        shutil.copy(resultsFolder / maskFileName, maskOutput / Path(indexString + '-mask-' + filename[:-21] + '3.png') )
        shutil.copy(resultsFolder / cloudFileName, cloudOutput / Path(indexString + '-cloud-' + filename[:-21] + '3.png') )
        print('>    Fetched Mask & Cloud ', indexString)
        index = index + 1

finish_cyclegan()