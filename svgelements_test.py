# https://github.com/meerk40t/svgelements 참고
import math
import numpy
import os
from svgelements import *
from PIL import Image
import matplotlib.pyplot as plt

import svgelements_test

svg_file = './test_files/93.svg'

def bezierCurve(points):
    p1 = points[0]
    p2 = points[1]
    p3 = points[2]

    iteration = numpy.arange(0, 1, 0.1)

    for t in iteration:
        point = math.pow(1-t, 2) * p1 + 2*t*(1-t)*p2 + math.pow(t, 2)*p3
        plt.scatter(point.x, point.y, s=1, color=color)

    #plt.show()


def pathLine(point):
    x1 = lastpoint.x
    x2 = point.x
    y1 = lastpoint.y
    y2 = point.y

    if x1 != x2:
        m = (y2 - y1) / (x2 - x1)
        n = y1 - (m * x1)
        x = numpy.arange(x1, x2, (x2-x1)/100)
        y = [(m * num + n) for num in x]
        plt.scatter(x, y, s=1, color=color)

    elif y1 != y2:
        yList = numpy.arange(y1, y2, (y2-y1)/100)
        for y in yList:
            plt.scatter(x1, y, s=1, color=color)
    #plt.show()

def polyLine(points):
    for i in range(0, len(points)-1):
        x1 = points[i].x
        y1 = points[i].y
        x2 = points[i+1].x
        y2 = points[i+1].y

        if x2 != x1:
            m = (y2 - y1) / (x2 - x1)
            n = y1 - (m * x1)
            x = numpy.arange(x1, x2, (x2-x1)/100)
            y = [(m * num + n) for num in x]
            plt.scatter(x, y, s=1, color=color)

        else:
            yList = numpy.arange(y1, y2, (y2-y1)/100)
            for y in yList:
                plt.scatter(x1, y, s=1, color=color)
        #plt.show()

def simpleLine(points):
    x1 = points[0]
    y1 = points[1]
    x2 = points[2]
    y2 = points[3]

    if x2 != x1:
        m = (y2-y1)/(x2-x1)
        n = y1 - (m*x1)
        x = numpy.arange(x1, x2, (x2-x1)/100)
        y = [(m*num + n) for num in x]
        plt.scatter(x, y, s=1, color=color)

    else:
        yList = numpy.arange(y1, y2, (y2-y1)/100)
        for y in yList:
            plt.scatter(x1, y, s=1, color=color)
        #plt.show()

def circle(tag):

    numlist = numpy.arange(0, 360, 36)

    for theta in numlist:
        x = tag.cx + tag.rx*numpy.cos(numpy.radians(theta))
        y = tag.cy + tag.ry*numpy.sin(numpy.radians(theta))
        plt.scatter(x, y, s=1, color=color)

def get_data(tag):
    pathDatas = []

    if isinstance(tag, Path):
        data = tag.d()
        #print(data)
        global idx
        global pidx
        global lastpoint
        global secondControlPoint
        global isLastpoint
        points = []
        isLastpoint = False
        idx = 0

        for pathData in data:
            if pathData == 'M' or pathData == 'c' or pathData == 'C' or pathData == 's' or pathData == 'l' or \
                    pathData == 'L' or pathData == 'z' or pathData == 'h' or pathData == 'H' or pathData == 'S':
                pathDatas.append(pathData)

        for point in tag.as_points():
            if isLastpoint:
                lastpoint = point
                idx += 1
                pidx = 0
                points.clear()
                isLastpoint = False

            elif pathDatas[idx] == 'M':
                isLastpoint = True

            elif pathDatas[idx] == 'C' or pathDatas[idx] == 'c':
                points.append(point)
                if pidx == 2:
                    bezierCurve(points=points)
                    isLastpoint = True
                    secondControlPoint = points[1]
                pidx += 1
            elif pathDatas[idx] == 's' or pathDatas[idx] == 'S':
                if pidx == 0:
                    points.append(secondControlPoint)
                elif pidx == 1:
                    points.append(point)
                elif pidx == 2:
                    points.append(point)
                    bezierCurve(points=points)
                    isLastpoint = True
            elif pathDatas[idx] == 'l' or pathDatas[idx] == 'L':
                pathLine(point)
                isLastpoint = True

            elif pathDatas[idx] == 'h' or pathDatas[idx] == 'H':
                pathLine(point)
                isLastpoint = True
    if isinstance(tag, SimpleLine):
        points = [tag.x1, tag.y1, tag.x2, tag.y2]
        simpleLine(points=points)

    if isinstance(tag, Polyline):
        polyLine(tag.points)

    if isinstance(tag, Polygon):
        polyLine(tag.points)

    if isinstance(tag, Circle):
        circle(tag)


def tag_to_string(tag):
    if isinstance(tag, Group):
        return 'Group'
    elif isinstance(tag, Path):
        get_data(tag)
        return 'Path'
    elif isinstance(tag, Line):
        get_data(tag)
        return 'Line'
    elif isinstance(tag, Polyline):
        get_data(tag)
        return 'Polyline'
    elif isinstance(tag, Polygon):
        get_data(tag)
        return 'Polygon'
    elif isinstance(tag, SimpleLine):
        get_data(tag)
        return 'SimpleLine'
    elif isinstance(tag, Rect):
        get_data(tag)
        return 'Rect'
    elif isinstance(tag, Circle):
        get_data(tag)
        return 'Circle'
    else:
        return '??'

def tag_traverse(tag, level):
    global colors
    global color
    global coloridx
    global width
    global height

    colors = ['#e35f62', '#006400', '#ADFF2F', '#4682B4', '#9932CC', '#A9A9A9', "#2F4F4F", '#FF8C00', 'M80K80', 'M80C10'
              , '000000']
    indent = ''
    for i in range(level):
        indent = indent + '-'
    if level == 2:
        color = colors[coloridx]
        coloridx += 1

        plt.xlim(0, width)
        plt.ylim(0, height)
        plt.gca().invert_yaxis()
        plt.show()

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

coloridx = 0

width = SVG.parse(svg_file).width
height = SVG.parse(svg_file).height

for element in SVG.parse(svg_file):
    tag_traverse(element, 0)


plt.xlim(0, width)
plt.ylim(0, height)
plt.gca().invert_yaxis()
plt.show()



