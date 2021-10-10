
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class svgToimage() :
    def __init__(self, path):
        super().__init__()
        self.path = path

    def svgConvert(self):
        svg = svg2rlg(path=self.path)
        renderPM.drawToFile(svg, 'test.jpg', fmt='JPG')


if __name__ == '__main__':
   path = input()
   converter = svgToimage(path=path)
