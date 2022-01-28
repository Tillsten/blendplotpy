import attr
import numpy as np
from blendpy import make_path, g


@attr.s(auto_attribs=True, slots=True)
class Line:
    x: np.ndarray
    y: np.ndarray
    color: int
    linewidth: float = 1
    path: g.BLPath = attr.ib(factory=g.BLPath)

    def set_data(self, x, y):
        self.x, self.y = x, y

    def draw(self, ctx):
        ctx.save()
        ctx.setStrokeStyle(g.BLRgba32(self.color))
        ctx.setStrokeWidth(self.linewidth)
        self.path.reset()
        make_path(self.x.astype('f'), self.y.astype('f'),  self.path)
        ctx.strokePath(self.path)
        ctx.restore()
