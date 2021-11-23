import pyvips
import os
import sys
from svgs_to_image import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# python main.py 300
if __name__ == '__main__':
    inputPath = sys.argv[1]
    inputDpi = int(sys.argv[2])

    converter = svgToImage(path=inputPath)
    converter.svgConvert()
