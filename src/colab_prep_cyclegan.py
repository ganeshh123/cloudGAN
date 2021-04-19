import sys
from pathlib import Path
from shutil import copytree

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
rgbPath = userDataPath / 'rgb_store'
masksPath = userDataPath / 'mask_store'
inputFolder = userDataPath / 'cyclegan_input'
outputFolder = userDataPath / 'cyclegan_output'

def prep_cyclegan():
    copytree(masksPath / 'percentage95', (inputFolder / 'testB'))
    copytree(rgbPath  / 'percentage95', (inputFolder / 'testA'))

prep_cyclegan()