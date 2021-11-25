import pyvips
import os
import sys
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class svg_to_image() :
    def __init__(self, path, dpi):
        super().__init__()
        self.path = path
        self.dpi = dpi

    def svg_convert(self, src, dest):
        image = pyvips.Image.new_from_file(src, dpi = self.dpi)
        print("Converting {0}".format(src) + " in " + dest)
        image.write_to_file(dest) # fill none으로 되면 배경이 transparency.

    def convert_folder(self, cur_path, dest_path):
        next_file_list = os.listdir(cur_path)

        for next_file in next_file_list:
            next_file_path = cur_path + '/' + next_file
            next_dest_path = dest_path + '/'

            if os.path.isdir(next_file_path):
                next_dest_path += next_file
                try:
                    if not os.path.exists(next_dest_path):
                        os.makedirs(next_dest_path)
                    self.convert_folder(next_file_path, next_dest_path)
                except OSError:
                    print ('Error: Creating directory ' + next_dest_path + '.')

            elif os.path.isfile(next_file_path):
                tmpList = next_file.split('.')
                extension = tmpList[1]
                if extension == "svg":
                    new_file_name = tmpList[0] + '.png'
                    next_dest_path += new_file_name
                    self.svg_convert(next_file_path, next_dest_path)
                else:
                    print(next_file + "is not .svg file.")
                    continue

# argv = [input_path, output_path, dpi]
if __name__ == '__main__':
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    inputDpi = int(sys.argv[3])

    converter = svg_to_image(inputPath, inputDpi)
    converter.convert_folder(converter.path, outputPath)