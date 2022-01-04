
import sys
import ezdxf
from ezdxf import math
from PIL import Image, ImageDraw


doc = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'

msp = doc.modelspace()  # add new entities to the modelspace


msp.add_lwpolyline([(0, 0, 0), (10, 0, 1), (20, 0, 0), (20, 20, 1), (0, 20, 0), (0, 0, 0)], format='xyb')


doc.saveas('lwpoly.dxf')


try:
    doc1 = ezdxf.readfile("lwpoly.dxf")
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    sys.exit(2)

msp = doc1.modelspace()


pts = []



for i in msp:
    if i.dxftype() == 'LWPOLYLINE':
        pts = i.get_points('xyb')


class Arc_atts:

    def __init__(self, pts_in, res, offsetX=200, offsetY=200):
        self.pts_in = pts_in
        self.res = res
        self.offsetX = offsetX
        self.offsetY = offsetY

    def draw_arc(self):
        arcs = []
        for i in range(len(self.pts_in)):
            if self.pts_in[i][-1] != 0:
                arcs.append([self.pts_in[i], self.pts_in[i + 1]])
        return arcs

    def centers(self, arc_i):
        return ezdxf.math.bulge_to_arc((self.draw_arc()[arc_i][0][0]*self.res+self.offsetX, self.draw_arc()[arc_i][0][1]*self.res+self.offsetY),
                                       (self.draw_arc()[arc_i][1][0]*self.res+self.offsetX, self.draw_arc()[arc_i][1][1]*self.res+self.offsetY),
                                       self.draw_arc()[arc_i][0][2])[0]
    def radius(self, arc_i):
        return ezdxf.math.bulge_to_arc((self.draw_arc()[arc_i][0][0]*self.res+self.offsetX, self.draw_arc()[arc_i][0][1]*self.res+self.offsetY),
                                       (self.draw_arc()[arc_i][1][0]*self.res+self.offsetX, self.draw_arc()[arc_i][1][1]*self.res+self.offsetY),
                                       self.draw_arc()[arc_i][0][2])[3]

    def start_angle(self, arc_i):
        return int(ezdxf.math.bulge_to_arc((self.draw_arc()[arc_i][0][0], self.draw_arc()[arc_i][0][1]),
                                       (self.draw_arc()[arc_i][1][0], self.draw_arc()[arc_i][1][1]),
                                       self.draw_arc()[arc_i][0][2])[1]*180/3.14)

    def end_angle(self, arc_i):
        return int(ezdxf.math.bulge_to_arc((self.draw_arc()[arc_i][0][0], self.draw_arc()[arc_i][0][1]),
                                       (self.draw_arc()[arc_i][1][0], self.draw_arc()[arc_i][1][1]),
                                       self.draw_arc()[arc_i][0][2])[2]*180/3.14)

    def bounding_box(self, arc_i):
        return list(map(lambda x: x - self.radius(arc_i), self.centers(arc_i))) + list(map(lambda x: x + self.radius(arc_i), self.centers(arc_i)))


res = 5

t = Arc_atts(pts, res, offsetX=200, offsetY=200)


out = Image.new("RGB", (400, 400), (255, 255, 255))


d = ImageDraw.Draw(out)

for i in range(2):
    d.chord(t.bounding_box(i), t.start_angle(i), t.end_angle(i), fill='blue')

out.show()










