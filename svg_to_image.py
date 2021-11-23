import pyvips
import os
import sys
import shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class svgToImage() :
    def __init__(self, path, dpi):
        super().__init__()
        self.path = path
        self.dpi = dpi

    def svgConvert(self, src, dest):
        image = pyvips.Image.new_from_file(src, dpi = self.dpi)
        image.write_to_file(dest) # fill none으로 되면 배경이 transparency.

    def convertFolder(self, curPath, destPath):
        nextFileList = os.listdir(curPath)

        for nextFile in nextFileList:
            nextFilePath = curPath + '/' + nextFile
            nextDestPath = destPath + '/'

            if os.path.isdir(nextFilePath):
                nextDestPath += nextFile
                try:
                    if not os.path.exists(nextDestPath):
                        os.makedirs(nextDestPath)
                    self.convertFolder(nextFilePath, nextDestPath)
                except OSError:
                    print ('Error: Creating directory. ' +  nextDestPath)

            elif os.path.isfile(nextFilePath):
                tmpList = nextFile.split('.')
                extension = tmpList[1]
                if extension == "svg":
                    newFileName = tmpList[0] + '.png'
                    nextDestPath += newFileName
                    self.svgConvert(nextFilePath, nextDestPath)
                else:
                    print(nextFile + "is not .svg file.")
                    continue

if __name__ == '__main__':
    inputPath = sys.argv[1]
    inputDpi = int(sys.argv[2])

    converter = svgToImage(inputPath, inputDpi)
    converter.convertFolder(converter.path, "newfolder")