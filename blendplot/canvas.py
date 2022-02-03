import time
from ctypes import c_void_p
from tkinter.tix import X_REGION

from qtpy.QtCore import QTimer, Qt, QThread
from qtpy.QtWidgets import QWidget, QApplication
from qtpy.QtGui import QImage, QPainter, QMouseEvent
import attr

from .blendpy import Matrix2D, Image, g, Point, Context, Rgba32, Box, Rect
from .axes import Axis

@attr.define(slots=False)
class Canvas:
    dpi: float = 72
    thread_count: int = 4
    size_inches: Rect = Point(4, 4)
    axis_list: list[Axis] = attr.Factory(list)
    blImage: Image = attr.attrib()

    pixel2inch: Matrix2D = attr.ib(init=False)
    inch2pixel: Matrix2D = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.generate_transforms(self.blImage.width(), self.blImage.height())

    @blImage.default
    def _default_image(self):
        im = Image(int(self.size_inches.x / self.dpi),
                   int(self.size_inches.y // self.dpi),
                   g.BL_FORMAT_PRGB32)
        return im
        
    def generate_transforms(self, w, h):
        p = Point(w, h)
        p_in = p / self.dpi
        self.pixel2inch = Matrix2D.makeScaling(self.dpi)
        self.pixel2inch.scale(1, -1)
        self.pixel2inch.translate(0, -p_in.y)
        self.inch2pixel = Matrix2D(self.pixel2inch)
        self.inch2pixel.invert()

    def bl_paint(self):
        ci = g.BLContextCreateInfo()
        ci.threadCount = self.thread_count
        ctx = Context()
        ctx.begin(self.blImage, ci)
        ctx.setFillStyle(Rgba32(0xFF000000))
        ctx.fillAll()
        ctx.setCompOp(g.BL_COMP_OP_SRC_OVER)
        ctx.setStrokeTransformOrder(g.BL_STROKE_TRANSFORM_ORDER_BEFORE)
        ctx.transform(self.pixel2inch)
        for ax in self.axis_list:
            ax.draw(ctx)
        ctx.end()

    def make_axis(self):
        ax = Axis(0.14, 0.14, self.size_inches.x - 1, self.size_inches.y - 1)
        self.axis_list.append(ax)
        return ax



@attr.define(slots=False)
class CanvasQT(QWidget, Canvas):
    qtImage: QImage = attr.attrib(factory=QImage)    
    t0: float = attr.Factory(time.time)
    xlim: list[float] = [-10, 10]
    ylim: list[float] = [10, -10]
    dragging: bool = False
    zooming: bool = False   
    
    def __attrs_pre_init__(self):
        super().__init__()
        self.dpi = self.logicalDpiX()

    def dt(self):
        return time.time() - self.t0

    def resizeEvent(self, ev):
        w, h = self.width(), self.height()
        self.dpi = self.logicalDpiX()
        if (w == self.qtImage.width() and h == self.qtImage.height()):
            return
        if (w == 0) or (h == 0):
            return

        self.qtImage = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
        self.blImage.createFromData(w, h, g.BL_FORMAT_PRGB32,
                                    c_void_p(int(self.qtImage.bits())),
                                    self.qtImage.bytesPerLine())
        self.size_inches = Point(w/self.dpi, h/self.dpi)
        self.generate_transforms(w, h)        
        self.axis_list[0].set_pos(0.18, 0.18, self.size_inches.x - 0.25, self.size_inches.y - 0.25)

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        self.bl_paint()
        painter.drawImage(0, 0, self.qtImage)

    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() == Qt.MidButton:
            self.dragging = True
            self.start = self.inch2pixel.mapPoint(ev.x(), ev.y())
            self.setMouseTracking(True)
        elif ev.button() == Qt.RightButton:
            self.zooming = True
            self.start_zooming = self.inch2pixel.mapPoint(ev.x(), ev.y())
            self.setMouseTracking(True)

    def mouseReleaseEvent(self, ev: QMouseEvent):
        if (ev.button() == Qt.MidButton):
            ev.accept()
            self.dragging = False
            self.setMouseTracking(False)
        elif ev.button() == Qt.RightButton:
            self.zooming = False
            self.setMouseTracking(False)

    def mouseMoveEvent(self, ev: QMouseEvent):
        pos = self.inch2pixel.mapPoint(ev.x(), ev.y())
        ax = self.axis_list[0]
        if self.dragging:
            dx = pos - self.start
            dxd = ax.data2inch.mapVector(dx)
            ax.set_viewlim(ax.view_lim - dxd)
            self.start = pos
            self.bl_paint()
        if self.zooming:
            dx = pos - self.start_zooming
            dxd = -ax.data2inch.mapVector(dx)
            ax.set_viewlim(ax.view_lim *
                                  (1+0.1*dxd))
            self.start_zooming = pos
            self.bl_paint()

