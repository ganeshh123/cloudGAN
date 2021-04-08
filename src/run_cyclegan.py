import sys
import os
from pathlib import Path
from numpy import loadtxt

userDataPath = Path(sys.path[0]).resolve() / '..' / 'userdata'
staticDataPath = Path(str(loadtxt(userDataPath / 'staticDataPath.txt', dtype='str')))
networkName = 'mask-cloud-networks'
inputFolder = userDataPath / 'cyclegan_input'
outputFolder = userDataPath / 'cyclegan_output'


def run_cyclegan():
    cycleganCommand = 'python cyclegan/test.py'
    cycleganCommand += ' --dataroot ' + str(inputFolder.resolve())
    cycleganCommand += ' --name ' + networkName
    cycleganCommand += ' --model cycle_gan'
    cycleganCommand += ' --checkpoints_dir ' + str(staticDataPath.resolve())
    cycleganCommand += ' --gpu_ids -1'
    cycleganCommand += ' --results_dir ' + str(outputFolder.resolve())
    cycleganCommand += ' --num_test 3500'
    cycleganCommand += ' --load_size 200'
    cycleganCommand += ' --crop_size 200'

    print(cycleganCommand)
    os.system(cycleganCommand)


run_cyclegan()