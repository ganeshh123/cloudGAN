from pathlib import Path
from shutil import copytree

userDataPath = Path().resolve() / '..' / 'userdata'
rgbPath = userDataPath / 'rgb_store'
masksPath = userDataPath / 'mask_store'
inputFolder = userDataPath / 'cyclegan_input'
outputFolder = userDataPath / 'cyclegan_output'

def prep_cyclegan():
    copytree(masksPath / 'percentage99', (inputFolder / 'testB'), dirs_exist_ok=True)
    copytree(rgbPath  / 'percentage99', (inputFolder / 'testA'), dirs_exist_ok=True)

prep_cyclegan()