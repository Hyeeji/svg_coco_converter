import os
import sys
import json
import time
import xml.etree.ElementTree as ET
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.svg_process import gather_name_from_first_level_node
from common.svg_cleaner import correct_id

data = {}
data['categories'] = []

BASE = 'base'
STICKER = 'sticker'


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


def is_base(category):
    category = category[:-1]
    for base in category_base_names:
        if category == base:
            print(category)
            return True
    return False


def get_category_names(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()

    segment_names = []
    # First gather names for each base/sticker
    for first_lvl in root:
        segment_names.append(gather_name_from_first_level_node(first_lvl))

    return segment_names


def fetch_category(root):
    entire_category = set()
    # No need to traverse path when fetching only categories
    for full_dir, dirs, files in os.walk(root):
        for name in files:
            if name.endswith((".svg")):
                folder = str(full_dir).split(root)
                folder_ = str(folder[1]).split('\\')
                folder_name = folder_[2]

                svg_path = os.path.join(full_dir, name)
                print('Processing {}...'.format(svg_path))
                name_list = get_category_names(svg_path)

                for category_name in name_list:
                    correct_category = correct_id(category_name)
                    if correct_category == "":
                        continue
                    else:
                        category_name = folder_name + '-' + correct_category
                        if is_base(category_name):
                            category_name = category_name + BASE
                        else:
                            category_name = category_name + STICKER

                        entire_category.add(category_name)

    print('Total number of category fetched: {}'.format(len(entire_category)))
    return entire_category


def dump_category_result(out_path, entire_category):
    id = 0
    for cat in entire_category:
        # TODO: add supercategory if required
        data['categories'].append({'id': id, 'name': correct_id(cat)})
        id += 1

    with open(out_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    start = time.time()
    DATA_ROOT = 'D:/Test_Models/FAAI'
    OUT_PATH = '../../../test_files/categories.json'
    XLS_PATH = 'D:/Pattern_dataset/svg_database+pattern_code_ver4.xlsx'

    category_base_names = fetch_base(XLS_PATH)
    entire_category = fetch_category(DATA_ROOT)
    dump_category_result(OUT_PATH, entire_category)

    print(time.time() - start)
