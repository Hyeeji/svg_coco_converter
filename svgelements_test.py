# https://github.com/meerk40t/svgelements 참고

import os
import matplotlib.pyplot as plt
from svgelements import *
import cv2
import numpy as np

from svg_path_to_polygons import svg_path_to_polygons

# svg_file = './test_files/0_Segment/0_open.svg'
svg_file = './test_files/93.svg'

def tag_to_string(tag):
    tag_str = ''

    if isinstance(tag, Group):
        tag_str = 'Group'
    elif isinstance(tag, Path):
        tag_str = 'Path'
    elif isinstance(tag, Line):
        tag_str = 'Line'
    elif isinstance(tag, Polyline):
        tag_str = 'Polyline'
    elif isinstance(tag, Polygon):
        tag_str = 'Polygon'
    elif isinstance(tag, SimpleLine):
        tag_str = 'SimpleLine'
    else:
        tag_str = '??'

    return tag_str

def tag_get_polygons(tag):
    poly_points = []

    if isinstance(tag, Path):
        poly_points = svg_path_to_polygons(tag)
    elif isinstance(tag, SimpleLine):
        poly_points.append([Point(tag.x1, tag.y1), Point(tag.x2, tag.y2)])
    elif isinstance(tag, Polyline):
        polygon = []
        for point in tag.points:
            polygon.append(Point(point.x, point.y))
        poly_points.append(polygon)
    elif isinstance(tag, Polygon):
        polygon = []
        for point in tag.points:
            polygon.append(Point(point.x, point.y))
        poly_points.append(polygon)

    return poly_points

def tag_traverse(tag, level, polygons):
    indent = ''
    for i in range(level):
        indent = indent + '-'

    if tag.id == None:
        tag_name = 'None'
    else:
        tag_name = tag.id

    tag_str = tag_to_string(tag)
    polygons.append(tag_get_polygons(tag))
    print(indent + tag_name + '(' + tag_str + ')')

    if isinstance(tag, Group) == False:
        return None
    else:
        for t in tag:
            tag_traverse(t, level+1, polygons)


if __name__ == '__main__':
    img = cv2.imread('test_files/0.png', cv2.IMREAD_UNCHANGED)
    cv2.resize(img, dsize=(595,841))

    width = SVG.parse(svg_file).width
    height = SVG.parse(svg_file).height

    for element in SVG.parse(svg_file):
        polygons = []
        tag_traverse(element, 0, polygons)
        # plt.close()
        # plt.imshow(img)
        plt.xlim(0, width)
        plt.ylim(0, height)
        plt.gca().invert_yaxis()
        for polygon in polygons:
            if len(polygon) is not 0:
                x_vals = []
                y_vals = []
                for segment in polygon:
                    for point in segment:
                        x_vals.append(point.x)
                        y_vals.append(point.y)

                # x_vals.append(x_vals[0]) # force closing
                # y_vals.append(y_vals[0])  # force closing

                plt.plot(x_vals, y_vals)

        plt.show()




