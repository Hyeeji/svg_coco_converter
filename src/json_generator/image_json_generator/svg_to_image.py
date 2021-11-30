import os
import sys
from pyvips import Image

def svg_convert(src, dest, dpi):
    image = Image.new_from_file(src, dpi = dpi)
    print("Converting {0} into {1}".format(src, dest))
    image.write_to_file(dest) # fill none으로 되면 배경이 transparency.

    return image.width, image.height