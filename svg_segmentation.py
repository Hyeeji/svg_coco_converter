import xml.etree.ElementTree as ET
import copy
import os

def gather_name(node):
    if 'path' in node.tag or 'line' in node.tag or 'polyline' in node.tag or 'polygon' in node.tag:
        return ""
    else:
        for subnode in node:
            if "id" in node.attrib:
                return node.attrib["id"] + "-" + gather_name(subnode)
            else:
                return "" + gather_name(subnode)

def change_fill_style(node):
    if 'style' in node.attrib:
        start_idx = node.attrib['style'].find('fill:')
        if start_idx is not -1:
            end_idx = node.attrib['style'].find(';',start_idx)
            node.attrib['style'] = node.attrib['style'].replace(node.attrib['style'][start_idx:end_idx], "fill:#000000")
    for subnode in node:
        change_fill_style(subnode)

if __name__ == '__main__':
    input_path = './test_files'
    output_path = './segmented_files'
    file_name = '0'
    extention = '.svg'

    svg_file = os.path.join(input_path,file_name + extention)

    ET.register_namespace('', "http://www.w3.org/2000/svg")
    tree = ET.parse(svg_file)
    root = tree.getroot()
    change_fill_style(root)

    segment_names = []
    for first_lvl in root:
        segment_names.append(gather_name(first_lvl))

    for i in range(len(root)):
        tree_cpy = copy.deepcopy(tree)
        export_root = tree_cpy.getroot()
        for first_lvl in list(export_root):
            export_root.remove(first_lvl)

        export_root.append(root[i])

        out_folder = os.path.join(output_path, file_name)
        if not os.path.exists(out_folder):
            os.mkdir(out_folder)
        tree_cpy.write("{0}/{1}_{2}{3}".format(out_folder, file_name, segment_names[i], extention), encoding="ASCII", xml_declaration=True)





