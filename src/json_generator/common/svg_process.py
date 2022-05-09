import xml.etree.ElementTree as ET

def gather_name_from_first_level_node(node):
    # Recursively gather name(=id)s for each base/sticker
    # node : first level node of SVG file

    if "id" in node.attrib:
        if node.attrib["id"] == 'None' or node.attrib["id"] == 'None_2_' or node.attrib["id"] == 'None_1_' \
                or node.attrib["id"] == 'None_3_':
            return ""

    if 'path' in node.tag or 'line' in node.tag or 'polyline' in node.tag or 'polygon' in node.tag\
            or 'rect' in node.tag:
        # Does not care about geometry tag name
        return ""
    else:
        if len(node) == 0:
            return ""
        for subnode in node:
            if "id" in node.attrib:
                # Concatenate current name and call gather_name on child
                return node.attrib["id"] + "-" + gather_name_from_first_level_node(subnode)
            else:
                # If current tag does not have a name, just call on child
                return "" + gather_name_from_first_level_node(subnode)