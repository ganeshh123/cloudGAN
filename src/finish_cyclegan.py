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

    index = 1
    for filename in os.listdir(resultsFolder):
        indexString = str(index).zfill(5)
        if '_real_B' in filename:
            masks.append(filename)
            print('Getting mask ' + indexString)
            shutil.copy(resultsFolder / filename, maskOutput / Path(indexString + '-mask.jpg') )
            index = index + 1
        elif '_fake_A' in filename:
            clouds.append(filename)
            print('Getting cloud ' + indexString)
            shutil.copy(resultsFolder / filename, cloudOutput / Path(indexString + '-cloud.jpg') )

finish_cyclegan()