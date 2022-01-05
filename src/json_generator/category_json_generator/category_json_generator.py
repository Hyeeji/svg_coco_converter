import os
import sys
import json
import xml.etree.ElementTree as ET
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.svg_process import gather_name_from_first_level_node
from common.svg_cleaner import correct_id

data = {}
data['categories'] = []

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
                svg_path = os.path.join(full_dir, name)
                print('Processing {}...'.format(svg_path))
                name_list = get_category_names(svg_path)
                entire_category.update(set(name_list))

    print('Total number of category fetched: {}'.format(len(entire_category)))
    return entire_category

def dump_category_result(out_path, entire_category):
    categories = []

    id = 0
    for cat in entire_category:
        # TODO: add supercategory if required
        data['categories'].append({'id': id, 'name': correct_id(cat)})
        id += 1

    with open(out_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    # DATA_ROOT = 'D:/Test_Models/FAAI/Dataset'
    # DATA_ROOT = 'D:/Test_Models/FAAI/test'
    # OUT_PATH = '../../../test_files/categories.json'
    DATA_ROOT = 'C:\\Users\\tuna1\\Documents\\AIFasion\\test_folder'
    OUT_PATH = 'C:\\Users\\tuna1\\Documents\\AIFasion\\test_folder\\categories.json'

    entire_category = fetch_category(DATA_ROOT)
    dump_category_result(OUT_PATH, entire_category)
