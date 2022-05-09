from src.json_generator.common.svg_process import gather_name_from_first_level_node
from src.json_generator.common.svg_cleaner import correct_id
import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
import json
import tqdm

BASE = 'base'
STICKER = 'sticker'

#파일 이름 추출하는 코드

def is_base(category):
    category = category[:-1]
    for base in category_base_names:
        if category == base:
            return True
    return False


def concat_string_with(delim, *arg):
    result = ''
    for s in arg:
        result += s
        result += delim

    return result[:-1]


def fetch_base(xls_path):
    base_sheet = pd.read_excel(xls_path, sheet_name=0, header=0, engine='openpyxl')
    category_names = []
    num_record = len(base_sheet['svg_name'])
    for i in range(num_record):
        full_name = concat_string_with('-', base_sheet['garment_type'][i], base_sheet['layer1'][i],
                                       base_sheet['layer2'][i], base_sheet['layer3'][i])
        category_names.append(full_name)

    return category_names


def get_category_names(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    segment_names = []
    # First gather names for each base/sticker
    for first_lvl in root:
        aa = correct_id(gather_name_from_first_level_node(first_lvl))
        if aa != '':
            segment_names.append(aa)
    return segment_names


if __name__ == '__main__':
    XLS_PATH = 'D:/Pattern_dataset/svg_database+pattern_code_ver4.xlsx'
    category_base_names = fetch_base(XLS_PATH)
    with open('../../../test_files/categories.json', 'r') as f:
        category_json = json.load(f)
    category_name_to_id = dict()
    category_id_and_imgs = dict()
    for cat in category_json['categories']:
        category_name_to_id[cat['name']] = cat['id']
        category_id_and_imgs[cat['id']] = []
    img_root =  'D:/Test_Models/FAAI'
    img_root_path = Path(img_root)

    svg_path_list = list(img_root_path.glob('**/*.svg'))

    for img_path in tqdm.tqdm(svg_path_list):
        str_img_path = str(img_path)

        img_name = '/'.join(str_img_path.split(sep='\\')[3:])

        folder_name = img_name.split('/')
        folder_name = folder_name[1]

        for category_name in get_category_names(str_img_path):
            category_name = folder_name + '-' + category_name
            if is_base(category_name):
                category_name = category_name + BASE
            else:
                category_name = category_name + STICKER

            cat_id = category_name_to_id[category_name]
            category_id_and_imgs[cat_id].append(img_name)

    with open('category_names.json', 'w') as f:
        json.dump(category_id_and_imgs, f, indent=4)