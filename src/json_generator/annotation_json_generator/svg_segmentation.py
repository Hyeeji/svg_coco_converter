import xml.etree.ElementTree as ET
import copy
import os


def gather_name(node):
    # Recursively gather name(=id)s for each base/sticker

    if 'path' in node.tag or 'line' in node.tag or 'polyline' in node.tag or 'polygon' in node.tag:
        # Does not care about geometry tag name
        return ""
    else:
        for subnode in node:
            if "id" in node.attrib:
                # Concatenate current name and call gather_name on child
                return node.attrib["id"] + "-" + gather_name(subnode)
            else:
                # If current tag does not have a name, just call on child
                return "" + gather_name(subnode)

def change_fill_style(node):
    # Recursively change fill style as a black color, so that meaningful (internal) area is all presented in black

    if 'style' in node.attrib:
        start_idx = node.attrib['style'].find('fill:')
        if start_idx is not -1:
            end_idx = node.attrib['style'].find(';',start_idx)
            node.attrib['style'] = node.attrib['style'].replace(node.attrib['style'][start_idx:end_idx], "fill:#000000")
    for subnode in node:
        change_fill_style(subnode)

def get_segmentation_names():
    input_path = './test_files'
    file_name = '0'
    extention = '.svg'
    segment_names = []

    svg_file = os.path.join(input_path, file_name + extention)

    ET.register_namespace('', "http://www.w3.org/2000/svg")  # should add namespace
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # First gather names for each base/sticker
    for first_lvl in root:
        segment_names.append(gather_name(first_lvl))

    return segment_names

def segmentation():
    input_path = './test_files'
    output_path = 'test_files/segmented_files'
    file_name = '0'
    extention = '.svg'
    segment_names = []

    svg_file = os.path.join(input_path, file_name + extention)

    ET.register_namespace('', "http://www.w3.org/2000/svg") # should add namespace
    tree = ET.parse(svg_file)
    root = tree.getroot()
    change_fill_style(root)

    # First gather names for each base/sticker
    for first_lvl in root:
        segment_names.append(gather_name(first_lvl))

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
        out_folder = os.path.join(output_path, file_name)
        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        # Filename contains layer 1 & 2 & 3 information
        tree_cpy.write("{0}/{1}_{2}{3}".format(out_folder, file_name, segment_names[i], extention), encoding="ASCII", xml_declaration=True)