import os
import sys
from pathlib import Path
import json
import shutil

#2
#디렉토리 만드는 코드 & 실제로 이미지를 추출해서 저장하는 코드

if __name__ == "__main__":

    dir = 'D:/Test_Models/FAAI/'
    test_dir = 'D:/Test_Models/FAAI/test'
    segmented_dir = 'D:/Test_Models/FAAI/train_segmented_files'

    p = Path('D:/Test_Models/FAAI')

    dir_list = [i for i in p.glob('**')]
    dir_five = [i for i in p.glob('*')]

    for i in dir_list:
        #pp1 = Path(test_dir, *i.parts[3:])
        pp2 = Path(segmented_dir, *i.parts[3:])

        #pp1.mkdir(parents=True, exist_ok=True)
        pp2.mkdir(parents=True, exist_ok=True)

    '''with open('../category_json_generator/test_file_name.json', 'r') as f:
        test_category_list = json.load(f)

    for file_name in test_category_list:
        file = dir + file_name
        temp = file.split('FAAI')
        dest = test_dir + temp[1]

        shutil.copy(file, dest)
        print(file)'''


    '''for i in dir_five:
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
                    print(file)
                    os.remove(file)'''


