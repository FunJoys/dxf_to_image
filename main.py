
import sys
import ezdxf
from ezdxf import math
from PIL import ImageDraw


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

    def __init__(self, pts_in, res):
        self.pts_in = pts_in
        self.res = res

    def draw_arc(self):
        arcs = []
        for i in range(len(self.pts_in)):
            if self.pts_in[i][-1] != 0:
                arcs.append([self.pts_in[i], self.pts_in[i + 1]])
        return arcs

    def start_angle(self, i):
        return [ezdxf.math.bulge_to_arc(ezdxf.math.Vec2(self.draw_arc()[i][0][0], self.draw_arc()[i][1][0]), ezdxf.math.Vec2(self.draw_arc()[i][0][1], self.draw_arc()[i][1][1]), self.draw_arc()[i][0][2])[1]][0]

    def end_angle(self, i):
        return [ezdxf.math.bulge_to_arc(ezdxf.math.Vec2(self.draw_arc()[i][0][0], self.draw_arc()[i][1][0]), ezdxf.math.Vec2(self.draw_arc()[i][0][1], self.draw_arc()[i][1][1]), self.draw_arc()[i][0][2])[2]][0]

    def bounding_box(self, i):
        return [int(self.draw_arc()[i][0][0]*self.res), int(self.draw_arc()[i][0][1]*self.res), int(self.draw_arc()[i][1][0]*self.res), int(self.draw_arc()[i][1][1]*self.res)]




t = Arc_atts(pts, 100)

print(t.draw_arc())

print(t.bounding_box(0))
print(t.start_angle(0))









