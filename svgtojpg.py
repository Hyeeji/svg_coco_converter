import pyvips
import os
import shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class svgToimage() :
    def __init__(self, path):
        super().__init__()
        self.path = path

    def svgConvert(self):
        image = pyvips.Image.new_from_file("./test_files/66.svg", dpi=300)
        image.write_to_file("test1.png") # fill none으로 되면 배경이 transparency.

    def duplicateFolder(self, dpi):
        newFolderName = "./new_folder" + str(dpi)
        if not os.path.exists(newFolderName):
            shutil.copytree(self.path, newFolderName)
        self.docPath = newFolderName

if __name__ == '__main__':
    converter = svgToimage("./test_folder")
    converter.svgConvert()
    converter.duplicateFolder(300)