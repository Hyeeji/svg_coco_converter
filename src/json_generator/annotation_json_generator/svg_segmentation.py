import xml.etree.ElementTree as ET
import copy
import os


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
                # Concatenate current name and call gather_name on child

                # print(subnode)
                # print(subnode.attrib)
                # print(subnode.attrib["id"] == 'None' or subnode.attrib["id"] == 'None_2_' or subnode.attrib["id"] == 'None_1_' or subnode.attrib["id"] == 'None_3_')
                # print('path' in subnode.tag or 'line' in subnode.tag or 'polyline' in subnode.tag or 'polygon' in subnode.tag)
                # print("id" in subnode.attrib)
                # print([i for i in subnode])
                # print(type(gather_name(subnode)))
                # print()
                # <Element '{http://www.w3.org/2000/svg}rect' at 0x0000023B8648FDB8> 에 대하여 None return
                # {'id': 'close_184_', 'x': '-49.684', 'y': '-45.793', 'style': 'fill:#000000;', 'width': '101.968', 'height': '34.019'}
                # for subnode in node: 이 실행되는데 [i for i in subnode]은 [] 임, for subnode in node: 루프는 한번도 실행되지 않고 바로 끝남
                # 그래서 리턴되는 값이 없음 -> None이 되고 에러 발생. 따라서 39번줄에 return ""를 추가해줌 이런 동작이 맞는지는 혜지씨 판단 필요

                return node.attrib["id"] + "-" + gather_name(subnode)
            else:
                # If current tag does not have a name, just call on child
                return "" + gather_name(subnode)
        #rect에 subnode가 없어서 오류발생함
        return ""

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
    #DATA_ROOT = 'D:/Test_Models/FAAI/'
    DATA_ROOT = 'D:/Test_Models/FAAI/test'
    #input_path = 'D:/Test_Models/FAAI/test_small'
    output_root = 'D:/Test_Models/FAAI/segmented_files'
    #output_root = 'D:/Test_Models/segmented_files'
    extention = '.svg'
    segment_names = []

    for full_dir, dirs, files in os.walk(DATA_ROOT):
        for name in files:
            if name.endswith((".svg")):
                #print(name)
                file_name = name
                svg_path = os.path.join(full_dir, name)
                print(svg_path)

                ET.register_namespace('', "http://www.w3.org/2000/svg")  # should add namespace
                tree = ET.parse(svg_path)
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
                    path = os.path.dirname(svg_path)
                    path = path.split(sep=DATA_ROOT)
                    output_path = output_root + '/' + path[1]
                    output_path = output_path.replace('\\', '/')

                    #out_folder = os.path.join(output_path, file_name)
                    file_names = file_name.split('.')
                    file_name = file_names[0]
                    out_folder = output_path + '/' + file_name

                    if not os.path.exists(out_folder):
                        os.mkdir(out_folder)

        # Filename contains layer 1 & 2 & 3 information
                    tree_cpy.write("{0}/{1}_{2}{3}".format(out_folder, file_name, segment_names[i], extention),
                                   encoding="ASCII", xml_declaration=True)