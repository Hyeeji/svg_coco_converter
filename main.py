import pyvips
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class svgToimage() :
    def __init__(self, path):
        super().__init__()
        self.path = path

    def svgConvert(self):
        image = pyvips.Image.new_from_file(self.path, dpi=600)
        image.write_to_file("test.png") # fill none으로 되면 배경이 transparency.


if __name__ == '__main__':
    inputPath = './test_files/0_body.svg'

    converter = svgToimage(path=inputPath)
    converter.svgConvert()