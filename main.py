
import sys
import ezdxf
from ezdxf import math
from ezdxf import recover
from ezdxf.addons.drawing import matplotlib



doc = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'

msp = doc.modelspace()  # add new entities to the modelspace


msp.add_lwpolyline([(0, 0, 0), (10, 0, 1), (20, 0, 0), (20, 20, 1), (0, 20, 0), (0, 0, 0)], format='xyb', close=True)


doc.saveas('lwpoly.dxf')


try:
    doc1 = ezdxf.readfile("lwpoly.dxf")
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    sys.exit(2)




pts = []


for i in msp:
    if i.dxftype() == 'LWPOLYLINE':
        pts = i.get_points('xyb')



doc2 = ezdxf.new('R2000')  # hatch requires the DXF R2000 (AC1015) format or later
msp2 = doc2.modelspace()  # adding entities to the model space

hatch = msp2.add_hatch(color=1, dxfattribs={
    'hatch_style': ezdxf.const.HATCH_STYLE_NESTED})

hatch.paths.add_polyline_path(
    pts, is_closed=True,
    flags=ezdxf.const.BOUNDARY_PATH_EXTERNAL)

doc2.saveas("solid_hatch_polyline_path_with_bulge.dxf")


# Exception handling left out for compactness:
doc, auditor = recover.readfile("solid_hatch_polyline_path_with_bulge.dxf")
if not auditor.has_errors:
    matplotlib.qsave(doc.modelspace(), 'solid_hatch_polyline_path_with_bulge.png')



