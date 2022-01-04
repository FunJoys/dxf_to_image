import sys
import ezdxf
import matplotlib.pyplot as plt
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend


class GetData:
    def __init__(self, dxfname):
        self.dxfname = dxfname

    def read_dxf(self):
        try:
            doc1 = ezdxf.readfile(self.dxfname)
        except IOError:
            print(f'Not a DXF file or a generic I/O error.')
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print(f'Invalid or corrupted DXF file.')
            sys.exit(2)
        return doc1

    def get_polyline_data(self):
        msp = self.read_dxf().modelspace()  # add new entities to the modelspace
        pts = []
        for i in msp:
            if i.dxftype() == 'LWPOLYLINE' and i.dxf.layer == 'Top':
                pts.append(i.get_points('xyb'))
        return pts


class DrawDxf:
    def __init__(self, pts, dpi=300):
        self.pts = pts
        self.dpi = dpi
        self.Draw()

    def Draw(self):
        doc2 = ezdxf.new('R2000')  # hatch requires the DXF R2000 (AC1015) format or later
        msp2 = doc2.modelspace()  # adding entities to the model space
        hatch = msp2.add_hatch(color=1, dxfattribs={
            'hatch_style': ezdxf.const.HATCH_STYLE_NESTED})
        for i in range(len(self.pts)):
            hatch.paths.add_polyline_path(self.pts[i], is_closed=True, flags=ezdxf.const.BOUNDARY_PATH_EXTERNAL)

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc2)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(doc2.modelspace(), finalize=True)
        fig.savefig('your.png', dpi=self.dpi)





dxfname = "weibo.dxf"
dxf1 = GetData(dxfname)
pts = dxf1.get_polyline_data()
DrawDxf(pts, dpi=450)


