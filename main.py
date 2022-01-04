import sys
import ezdxf
from ezdxf import math
from PIL import Image, ImageDraw
import aggdraw


# create test dxf file
def create_dxf():
    doc = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'
    msp = doc.modelspace()  # add new entities to the modelspace
    msp.add_lwpolyline([(0, 0, 0), (10, 0, 1), (20, 0, 0), (20, 20, 1), (0, 20, 0), (0, 0, 0)], format='xyb')
    doc.saveas('lwpoly.dxf')


# get the dxf data
def get_dxf_data(dxfname):
    try:
        doc1 = ezdxf.readfile(dxfname)
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
    return pts


# draw an image from polylines data
pts = get_dxf_data('lwpoly.dxf')



out = Image.new("RGB", (400, 400), (255, 255, 255))
img = ImageDraw.Draw(out)

out = out.transpose(method=Image.FLIP_TOP_BOTTOM)

out.show()

