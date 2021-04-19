import sys
from pathlib import Path
from shutil import copytree

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
rgbPath = userDataPath / 'rgb_store'
masksPath = userDataPath / 'mask_store'
inputFolder = userDataPath / 'cyclegan_input'
outputFolder = userDataPath / 'cyclegan_output'

def prep_cyclegan():
    #Colab has some issues with using copytree
    copytree(masksPath / 'percentage95', (inputFolder / 'testB'), dirs_exist_ok=True)
    copytree(rgbPath  / 'percentage95', (inputFolder / 'testA'), dirs_exist_ok=True)

prep_cyclegan()