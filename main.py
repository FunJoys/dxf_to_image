
import sys
import ezdxf
import matplotlib.pyplot as plt
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend


try:
    doc1 = ezdxf.readfile("weibo.dxf")
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    sys.exit(2)

msp = doc1.modelspace()  # add new entities to the modelspace

pts = []


for i in msp:
    if i.dxftype() == 'LWPOLYLINE' and i.dxf.layer == 'Top':
        pts.append(i.get_points('xyb'))

print(pts)

doc2 = ezdxf.new('R2000')  # hatch requires the DXF R2000 (AC1015) format or later
msp2 = doc2.modelspace()  # adding entities to the model space

hatch = msp2.add_hatch(color=1, dxfattribs={
    'hatch_style': ezdxf.const.HATCH_STYLE_NESTED})

for i in range(len(pts)):
    hatch.paths.add_polyline_path(pts[i], is_closed=True, flags=ezdxf.const.BOUNDARY_PATH_EXTERNAL)




fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ctx = RenderContext(doc2)
out = MatplotlibBackend(ax)
Frontend(ctx, out).draw_layout(doc2.modelspace(), finalize=True)
fig.savefig('your.png', dpi=300)


