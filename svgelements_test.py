# https://github.com/meerk40t/svgelements 참고

import os
from svgelements import *

svg_file = './test_files/0.svg'

def tag_to_string(tag):
    if isinstance(tag, Group):
        return 'Group'
    elif isinstance(tag, Path):
        return 'Path'
    elif isinstance(tag, Line):
        return 'Line'
    elif isinstance(tag, Polyline):
        return 'Polyline'
    elif isinstance(tag, Polygon):
        return 'Polygon'
    elif isinstance(tag, SimpleLine):
        return 'SimpleLine'
    else:
        return '??'

def tag_traverse(tag, level):
    indent = ''
    for i in range(level):
        indent = indent + '-'

    if tag.id == None:
        tag_name = 'None'
    else:
        tag_name = tag.id

    print(indent + tag_name + '(' + tag_to_string(tag) + ')')

    if isinstance(tag, Group) == False:
        return None
    else:
        for t in tag:
            tag_traverse(t, level+1)


for element in SVG.parse(svg_file):
    tag_traverse(element, 0)

