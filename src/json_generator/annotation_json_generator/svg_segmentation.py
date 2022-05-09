import xml.etree.ElementTree as ET
import copy
import os
from src.json_generator.common.svg_process import gather_name_from_first_level_node
import pandas as pd
from src.json_generator.common.svg_cleaner import correct_id\


BASE = 'base'
STICKER = 'sticker'

def gather_name(node):
    # Recursively gather name(=id)s for each base/sticker
    if "id" in node.attrib:
        if node.attrib["id"] == 'None' or node.attrib["id"] == 'None_2_' or node.attrib["id"] == 'None_1_'\
                or node.attrib["id"] == 'None_3_':
            return ""

    if 'path' in node.tag or 'line' in node.tag or 'polyline' in node.tag or 'polygon' in node.tag:
        # Does not care about geometry tag name
        return ""
    else:
        for subnode in node:
            if "id" in node.attrib:
                return node.attrib["id"] + "-" + gather_name(subnode)
            else:
                # If current tag does not have a name, just call on child
                return "" + gather_name(subnode)
        return ""

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

def is_base(category, category_base_names):
    category = category[:-1]
    for base in category_base_names:
        if category == base:
            return True
    return False

def change_fill_style(node):
    # Recursively change fill style as a black color, so that meaningful (internal) area is all presented in black

    if 'style' in node.attrib:
        start_idx = node.attrib['style'].find('fill:')
        if start_idx is not -1:
            end_idx = node.attrib['style'].find(';',start_idx)
            node.attrib['style'] = node.attrib['style'].replace(node.attrib['style'][start_idx:end_idx], "fill:#000000")
    for subnode in node:
        change_fill_style(subnode)


def segmentation():
    DATA_ROOT = 'D:/Test_Models/FAAI/train'
    output_root = 'D:/Test_Models/FAAI/train_segmented_files'
    XLS_PATH = 'D:/Pattern_dataset/svg_database+pattern_code_ver4.xlsx'

    extention = '.svg'
    segment_names = []

    category_base_names = fetch_base(XLS_PATH)

    for full_dir, dirs, files in os.walk(DATA_ROOT):
        for name in files:
            if name.endswith((".svg")):
                file_name = name
                svg_path = os.path.join(full_dir, name)
                print(svg_path)

                ET.register_namespace('', "http://www.w3.org/2000/svg")  # should add namespace
                tree = ET.parse(svg_path)
                root = tree.getroot()
                change_fill_style(root)
    # First gather names for each base/sticker
                for first_lvl in root:
                    segment_names.append(gather_name_from_first_level_node(first_lvl))

    # Write each separated SVG file(sub-SVG) for base/sticker from source SVG
                for i in range(len(root)):
                    tree_cpy = copy.deepcopy(tree)
                    export_root = tree_cpy.getroot()
                    # Remove all children
                    for first_lvl in list(export_root):
                        export_root.remove(first_lvl)

                # Attach only one level 1 node
                    export_root.append(root[i])

                # Make folder for source svg file and write base/sticker sub-SVG file
                    path = os.path.dirname(svg_path)
                    path = path.split(sep=DATA_ROOT)

                    output_path = output_root + path[1]
                    output_path = output_path.replace('\\', '/')

                    folder_path = path[1].split('\\')
                    folder_name = folder_path[2]

                    file_names = file_name.split('.')
                    file_name = file_names[0]
                    out_folder = output_path + '/' + file_name

                    if not os.path.exists(out_folder):
                        os.mkdir(out_folder)

                    segment_name = folder_name + '-' + correct_id(segment_names[i])

                    if is_base(segment_name, category_base_names):
                        segment_name = segment_name + BASE
                    else:
                        segment_name = segment_name + STICKER

                    tree_cpy.write("{0}/{1}_{2}{3}".format(out_folder, file_name, segment_name, extention),
                                   encoding="ASCII", xml_declaration=True)
                segment_names.clear()


if __name__ == '__main__':
    segmentation()