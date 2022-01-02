import cv2
import sys
import ezdxf
from ezdxf import math
import numpy as np

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

    def __init__(self, pts_in):
        self.pts_in = pts_in

    def draw_arc(self):
        arcs = []
        for i in range(len(self.pts_in)):
            if self.pts_in[i][-1] != 0:
                arcs.append([self.pts_in[i], self.pts_in[i + 1]])
        return arcs

    def centers(self, i):
        return [ezdxf.math.bulge_to_arc(ezdxf.math.Vec2(self.draw_arc()[i][0][0], self.draw_arc()[i][1][0]), ezdxf.math.Vec2(self.draw_arc()[i][0][1], self.draw_arc()[i][1][1]), self.draw_arc()[i][0][2])[0]][0]

    def start_angles(self, i):
        return [ezdxf.math.bulge_to_arc(ezdxf.math.Vec2(self.draw_arc()[i][0][0], self.draw_arc()[i][1][0]), ezdxf.math.Vec2(self.draw_arc()[i][0][1], self.draw_arc()[i][1][1]), self.draw_arc()[i][0][2])[1]]







t = Arc_atts(pts)

print(t.draw_arc())

print(t.start_angles(1))











# height = 50
# width = 50
#
# img = np.zeros((height, width, 3), np.uint8)
#
# img[:, 0:width] = (255, 255, 255)      # (B, G, R)
#
# cv2.imshow('image', img)
# cv2.waitKey(0)








