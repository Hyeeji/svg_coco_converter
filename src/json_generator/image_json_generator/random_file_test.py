import os
import sys
from pathlib import Path
import shutil

if __name__ == "__main__":

    test_dir = 'D:/Test_Models/FAAI/test'
    segmented_dir = 'D:/Test_Models/FAAI/segmented_files'
    #segmented_dir = 'D:/Test_Models/segmented_files'
    p = Path('D:/Test_Models/FAAI')

    dir_list = [i for i in p.glob('**')]
    dir_five = [i for i in p.glob('*')]
    #print(dir_five)
    for i in dir_list:
        pp1 = Path(test_dir, *i.parts[3:])
        pp2 = Path(segmented_dir, *i.parts[3:])
        pp1.mkdir(parents=True, exist_ok=True)
        pp2.mkdir(parents=True, exist_ok=True)

    for i in dir_five:
        if str(i) != test_dir and str(i) != segmented_dir:
            li = [str(ii) for ii in i.glob('**/*.svg')]
            length = len(li)
            import random
            if length != 0:
                files = random.sample(li, 200)

                for file in files:
                    temp = file.split('FAAI')
                    dest = test_dir + temp[1]
                    dest = dest.replace('/', '\\')

                    shutil.copy(file, dest)

