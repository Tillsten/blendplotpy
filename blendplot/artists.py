import attr
import numpy as np
from .blendpy import make_path, g, Context

from typing import Protocol

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

    def draw(self, ctx: Context):
        ctx.save()
        ctx.setStrokeStyle(g.BLRgba32(self.edgecolor))
        ctx.setFillStyle(g.BLRgba32(self.facecolor))
        for xi, yi in zip(self.x, self.y):
            ctx.translate()
            
        ctx.restore()


@attr.define
class QuadMesh:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
