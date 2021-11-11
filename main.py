import pyvips
import os
import sys
from svgtojpg import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# python main.py 300
if __name__ == '__main__':
    inputPath = sys.argv[2]
    inputDpi = sys.argv[3]

    converter = svgToimage(path=inputPath)
    converter.svgConvert()
