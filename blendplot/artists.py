from __future__ import annotations
from pathlib import Path

import attr
import numpy as np
from .blendpy import Box, Matrix2D, make_path, g, Context, draw_scatter, Point, BLPath

from typing import ClassVar, Dict, Optional, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .axes import Axis

class Artist(Protocol):
    hit_path: Optional[BLPath] = None

    def draw(self, ctx: Context, parent: Axis):
        pass

    def get_limits(self, ctx: Context, parent: Axis) -> Optional[Box]:
        pass

    def is_hit(self, p: Point) -> bool:
        if self.hit_path:
            return self.hit_path.hitTest(p, g.BL_FILL_RULE_EVEN_ODD)
        else:
            return False


@attr.define
class Line(Artist):
    x: np.ndarray
    y: np.ndarray
    color: int
    linewidth: float = 1
    path: g.BLPath = attr.ib(factory=g.BLPath)

    def set_data(self, x, y):
        self.x, self.y = x, y
        self.path.reset()
        make_path(self.x.astype('f'), self.y.astype('f'),  self.path)

    def draw(self, ctx: Context, parent: Axis):
        ctx.save()
        ctx.setStrokeStyle(g.BLRgba32(self.color))
        ctx.setStrokeWidth(self.linewidth)
        ctx.strokePath(self.path)
        strokeOpts = g.BLStrokeOptions()
        strokeOpts.width = self.linewidth
        approx = g.blDefaultApproximationOptions
        self.hit_path = BLPath()
        ol = 'const BLPath& path, const BLStrokeOptionsCore& strokeOptions, const BLApproximationOptions& approximationOptions'
        f = self.hit_path.addStrokedPath.__overload__(ol)        
        f(self.path, strokeOpts, approx)
        ctx.restore()

    def get_limits(self, ctx: Context, parent: Axis) -> Optional[Box]:
        b = Box()
        self.path.getBoundingBox(b)        
        return b



def _make_symbol_paths():
    Path = g.BLPath

    rot_45 = g.BLMatrix2D()
    rot_45.resetToRotation(np.pi/4)

    rot_90 = Matrix2D.makeRotation(np.pi/2)

    box_path = Path()
    box_path.addBox(-0.5, -.5, .5, .5)

    diamond_path = Path()
    diamond_path.addBox(-0.5, -.5, .5, .5)
    diamond_path.transform.__overload__('const BLMatrix2D& m')(rot_45) 

    triangle_path = Path()
    triangle_path.addTriangle(g.BLTriangle(-.5, -.5, .5, -.5, 0, .5))
    triangle_path2 = Path(triangle_path)
    triangle_path2.transform.__overload__('const BLMatrix2D& m')(rot_90)
    triangle_path3 = Path(triangle_path2)
    triangle_path3.transform.__overload__('const BLMatrix2D& m')(rot_90)
    triangle_path4 = Path(triangle_path3)
    triangle_path4.transform.__overload__('const BLMatrix2D& m')(rot_90)


    circle_path = Path()
    circle_path.addCircle.__overload__('const BLCircle& circle, BLGeometryDirection dir = BL_GEOMETRY_DIRECTION_CW')(g.BLCircle(0, 0, .5))

    symbols = {
        '^': triangle_path,
        '>': triangle_path2,
        '<': triangle_path4,
        'v': triangle_path3,
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

    def draw(self, ctx: Context, parent: Axis):
        ctx.save()
        ctx.setStrokeStyle(g.BLRgba32(self.edgecolor))
        ctx.setStrokeWidth(self.linewidth)
        ctx.setFillStyle(g.BLRgba32(self.facecolor))
        p = self.symbols_list[self.symbol]        
        draw_scatter(ctx, p, self.x.astype('f8'), self.y.astype('f8'), self.size)
        ctx.restore()

    def set_data(self, x, y):
        self.x, self.y = x, y

    def get_limits(self, ctx: Context, parent: Axis) -> Optional[Box]:
        return Box(self.x.min(), self.y.min(), self.x.max(), self.y.max())

@attr.define
class QuadMesh:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
