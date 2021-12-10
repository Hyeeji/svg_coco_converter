import os
import sys
# from pyvips import Image
from cairosvg import svg2png

def svg_convert(src, dest, width, height):
    svg2png(url=src
            ,write_to=dest
            ,parent_width=width
            ,parent_height=height)
    # image = Image.new_from_file(src, dpi = dpi)
    print("Converting {0} into {1}".format(src, dest))
    # image.write_to_file(dest) # fill none으로 되면 배경이 transparency.

