
from math import pi
from typing import List, Optional
from attr import define, field
from math import pi, log10, ceil

from .artists import Artist, Line
from .blendpy import Box, Matrix2D, Point, Context, Rgba32, font, get_ticks, box_union
from .color import colors
from .ticks import get_ticks_talbot

AUTORANGE_PADDING = 1.1

@define
class Axis:
    x0: float
    y0: float
    w: float
    h: float
    box: Box = field(init=False)
    artists: List[Artist] = field(factory=list)
    
    view_lim: Box = Box(-5, -5, 10, 10)
    xticks: List[float] = field(factory=list)
    yticks: List[float] = field(factory=list)
    
    inch2data: Matrix2D = field(init=False)
    data2inch: Matrix2D = field(init=False)
    #pixel2data: Matrix2D = field(init=False)
    #data2pixel: Matrix2D = field(init=False)

    front_color: Rgba32 = Rgba32(colors['yellow'])
    bg_color: Rgba32 = Rgba32(0xFF000000)

    def __attrs_post_init__(self):
        self.generate_transforms()

    def set_pos(self, x0, y0, w, h):
        self.x0 = x0
        self.y0 = y0
        self.w, self.h = w, h
        
        self.generate_transforms()
        self.generate_ticks()

    def set_viewlim(self, view_lim):
        view_lim.x0 = max(-1e9, view_lim.x0)
        view_lim.x1 = min(1e9, view_lim.x1)
        view_lim.y0 = max(-1e9, view_lim.y0)
        view_lim.y1 = min(1e9, view_lim.y1)
        self.view_lim = view_lim
        self.generate_transforms()
        self.generate_ticks()

    def generate_transforms(self):
        self.box = Box(self.x0, self.y0, self.x0+self.w, self.y0+self.h)
        xs = self.view_lim.x1 - self.view_lim.x0
        ys = self.view_lim.y1 - self.view_lim.y0

        self.inch2data = Matrix2D.makeTranslation(self.x0, self.y0)
        self.inch2data.scale(self.w / xs, self.h / ys)
        self.inch2data.translate(-self.view_lim.x0, -self.view_lim.y0)

        self.data2inch = Matrix2D(self.inch2data)
        self.data2inch.invert()

    def generate_ticks(self):
        self.xticks = get_ticks_talbot(
            self.view_lim.x0, self.view_lim.x1, self.w)
        self.yticks = get_ticks_talbot(
            self.view_lim.y0, self.view_lim.y1, self.h)

    @property
    def x1(self):
        return self.x0 + self.w

    @property
    def y1(self):
        return self.y0 + self.h

    def add_artist(self, artist: Artist):
        self.artists.append(artist)

    def add_line(self, x, y, color, lw=2):
        if isinstance(color, str):
            color=colors[color]
        line = Line(x, y, color, linewidth=lw)
        self.artists.append(line)
        return line

    def draw(self, ctx):
        self.draw_self(ctx)
        self.draw_artists(ctx)

    def draw_self(self, ctx: Context):
        ctx.save()
        ctx.setFillStyle(self.bg_color)
        ctx.fillRect(self.x0, self.y0, self.w, self.h)
        ctx.setStrokeStyle(self.front_color)
        ctx.strokeRect(self.x0, self.y0, self.w, self.h)
        ctx.setFillStyle(self.front_color)

        if len(self.xticks) > 0:
            places = max(0, ceil(-log10(abs(self.xticks[1]-self.xticks[0]))))
            for i in self.xticks:
                p = self.inch2data.mapPoint(i, 0)
                p.y = self.y0
                ctx.strokeLine(p.x, self.y0, p.x, self.y0+0.05)
                ctx.save()
                ctx.translate(p)
                ctx.scale(-1, 1)
                ctx.rotate(-pi)
                txt = ("%%0.%df" % places) % i
                ctx.fillUtf8Text(Point(-0.00-len(txt)*0.03, .1), font, txt)
                ctx.restore()
                
        if len(self.yticks) > 0:
            places = max(0, ceil(-log10(abs(self.yticks[1]-self.yticks[0]))))
            for i in self.yticks:
                p = self.inch2data.mapPoint(0, i)
                p.x = self.x0
                ctx.strokeLine(self.x0, p.y, self.x0+0.05, p.y)
                ctx.save()
                ctx.translate(p)
                ctx.scale(-1, 1)
                ctx.rotate(pi)
                txt = ("%%0.%df" % places) % i
                ctx.fillUtf8Text(Point(-0.02-len(txt)*0.06, .04), font, txt)
                ctx.restore()
        
        ctx.restore()

    def draw_artists(self, ctx):
        ctx.save()
        ctx.clipToRect(self.x0, self.y0, self.w, self.h)
        ctx.transform(self.inch2data)        
        for a in self.artists:
            a.draw(ctx, self)
        ctx.restore()

    def autolimit(self):
        bboxes = [a.get_limits(None, self) for a in self.artists]
        self.set_viewlim(box_union(bboxes) * AUTORANGE_PADDING)            
    
    def scaleBy(self, center: Point, scale: Point):        
        bl = Point(self.view_lim.x0, self.view_lim.y0)
        tr = Point(self.view_lim.x1, self.view_lim.y1)
        trn = center + (tr-center) * scale
        bln = center + (bl-center) * scale      
        self.set_viewlim(Box(bln.x, bln.y, trn.x, trn.y))

    def is_hit(self, pos_in) -> Optional[Artist]:
        if self.box.contains(pos_in):
            data_coords = self.data2inch.mapPoint(pos_in)
            for a in self.artists:
                if a.is_hit(data_coords):
                    return a
        else:
            return None