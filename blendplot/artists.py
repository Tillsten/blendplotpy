import attr
import numpy as np
from .blendpy import make_path, g, Context, draw_scatter

from typing import ClassVar, Dict, Protocol

class Artist(Protocol):
    def draw(self, ctx: Context):
        pass


@attr.define
class Line:
    x: np.ndarray
    y: np.ndarray
    color: int
    linewidth: float = 1
    path: g.BLPath = attr.ib(factory=g.BLPath)

    def set_data(self, x, y):
        self.x, self.y = x, y
        self.path.reset()
        make_path(self.x.astype('f'), self.y.astype('f'),  self.path)

    def draw(self, ctx: Context):
        ctx.save()
        ctx.setStrokeStyle(g.BLRgba32(self.color))
        ctx.setStrokeWidth(self.linewidth)
        ctx.strokePath(self.path)
        ctx.restore()



def _make_symbol_paths():
    Path = g.BLPath

    rot_45 = g.BLMatrix2D()
    rot_45.resetToRotation(np.pi/4)

    box_path = g.BLPath()
    box_path.addBox(-0.5, -.5, .5, .5)

    diamond_path = g.BLPath()
    diamond_path.addBox(-0.5, -.5, .5, .5)
    diamond_path.transform.__overload__('const BLMatrix2D& m')(rot_45), 

    triangle_path = Path()
    triangle_path.addTriangle(g.BLTriangle(-.5, -.5, .5, -.5, 0, .5)),

    circle_path = Path()
    circle_path.addCircle.__overload__('const BLCircle& circle, BLGeometryDirection dir = BL_GEOMETRY_DIRECTION_CW')(g.BLCircle(0, 0, .5))

    symbols = {
        '^': triangle_path,
        's': box_path,
        'd': diamond_path,
        'o': circle_path,
    }
    return symbols

@attr.define
class Scatter(Artist):
    x: np.ndarray
    y: np.ndarray
    facecolor: int
    edgecolor: int
    linewidth: float = 1
    symbol: str = 'o'
    size: float = 3
    path: g.BLPath = attr.ib(factory=g.BLPath)
    symbols_list: ClassVar[Dict[str, g.BLPath]] = _make_symbol_paths()

    def draw(self, ctx: Context):
        ctx.save()
        ctx.setStrokeStyle(g.BLRgba32(self.edgecolor))
        ctx.setStrokeWidth(self.linewidth)
        ctx.setFillStyle(g.BLRgba32(self.facecolor))
        p = self.symbols_list[self.symbol]        
        draw_scatter(ctx, p, self.x.astype('f8'), self.y.astype('f8'), self.size)
        ctx.restore()

    def set_data(self, x, y):
        self.x, self.y = x, y


@attr.define
class QuadMesh:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
