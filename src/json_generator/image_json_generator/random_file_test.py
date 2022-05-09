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

    with open('../category_json_generator/test_file_name.json', 'r') as f:
        test_category_list = json.load(f)

    for file_name in test_category_list:
        file = dir + file_name
        temp = file.split('FAAI')
        dest = test_dir + temp[1]

        shutil.copy(file, dest)
        print(file)


