import re
import numpy
import math
import matplotlib.pyplot as plt
from svgelements import *

def bezierCurve(points):
    p1 = points[0]
    p2 = points[1]
    p3 = points[2]

    iteration = numpy.arange(0, 1, 0.1)

    curve_points = []
    for t in iteration:
        curve_points.append(math.pow(1-t, 2) * p1 + 2*t*(1-t)*p2 + math.pow(t, 2)*p3)
    return curve_points

def pathLine(point):
    x1 = lastpoint.x
    x2 = point.x
    y1 = lastpoint.y
    y2 = point.y

    curve_points = []
    if x1 != x2:
        m = (y2 - y1) / (x2 - x1)
        n = y1 - (m * x1)
        x = numpy.arange(x1, x2, (x2-x1)/10)
        y = [(m * num + n) for num in x]
        for element_idx in range(len(y)):
            curve_points.append(Point(x[element_idx], y[element_idx]))

    elif y1 != y2:
        yList = numpy.arange(y1, y2, (y2-y1)/10)
        for y in yList:
            curve_points.append(Point(x1,y))

    return curve_points

def svg_path_to_polygons(path_tag):
    path_str = path_tag.d().upper()

    global idx
    global pidx
    global lastpoint
    global secondControlPoint
    global isLastpoint
    isLastpoint = False
    idx = 0
    poly_points = []
    points = []

    start_point = []
    start_idx = 0

    pathDatas = []
    for pathData in path_tag.d().upper():
        if pathData == 'M' or pathData == 'C' or pathData == 'L' or pathData == 'Z' or pathData == 'H' or pathData == 'S':
            pathDatas.append(pathData)

    print(pathDatas)

    for point in path_tag.as_points():
        if start_idx is 0:
            start_point = point
            start_idx += 1

        if isLastpoint:
            lastpoint = point
            idx += 1
            pidx = 0
            points.clear()
            isLastpoint = False

        elif pathDatas[idx] == 'M':
            isLastpoint = True

        elif pathDatas[idx] == 'C':
            points.append(point)
            if pidx == 2:
                poly_points.append(bezierCurve(points=points))
                isLastpoint = True
                secondControlPoint = points[1]
            pidx += 1
        elif pathDatas[idx] == 'S':
            if pidx == 0:
                points.append(secondControlPoint)
            elif pidx == 1:
                points.append(point)
            elif pidx == 2:
                points.append(point)
                poly_points.append(bezierCurve(points=points))
                isLastpoint = True
        elif pathDatas[idx] == 'L':
            poly_points.append(pathLine(point))
            isLastpoint = True
        elif pathDatas[idx] == 'H':
            poly_points.append(pathLine(point))
            isLastpoint = True

    # print(poly_points)
    #
    # x_vals = []
    #     # y_vals = []
    #     # for poly_point in poly_points:
    #     #     for endpoint in poly_point:
    #     #         x_vals.append(endpoint.x)
    #     #         y_vals.append(endpoint.y)
    #     #
    #     # plt.plot(x_vals, y_vals)
    #     # plt.show()

    return poly_points