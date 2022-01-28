import time
from ctypes import c_void_p

from qtpy.QtCore import QTimer, Qt, QThread
from qtpy.QtWidgets import QWidget, QApplication
from qtpy.QtGui import QImage, QPainter, QMouseEvent
import attr
from sympy import Q


from axes import Axis
from blendpy import Matrix2D, Image, g, Point, Context, Rgba32

@attr.define
class Canvas(QWidget):
    qtImage: QImage = attr.attrib(factory=QImage)
    blImage: Image = attr.attrib(factory=Image)
    t0: float = attr.Factory(time.time)
    xlim: list[float] = [-10, 10]
    ylim: list[float] = [10, -10]
    dragging: bool = False
    zooming: bool = False
    dpi: float = 72

    def __attrs_post_init__(self):
        super().__init__()
        self.make_axis()

    def dt(self):
        return time.time() - self.t0

    def generate_transforms(self, w, h):
        p = Point(w, h)
        p_in = p / self.dpi
        self.pixel2inch = Matrix2D.makeScaling(self.dpi)
        self.pixel2inch.scale(1, -1)
        self.pixel2inch.translate(0, -p_in.y)
        self.inch2pixel = Matrix2D(self.pixel2inch)
        self.inch2pixel.invert()

    @property
    def size(self):
        w, h = self.width(), self.height()
        return Point((w / self.dpi), (h / self.dpi))

    def make_axis(self):
        self.axis = Axis(0.14, 0.1, self.size.x - 1, self.size.y - 1)

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
        self.generate_transforms(w, h)
        self.axis.set_pos(0.18, 0.18, self.size.x - 0.25, self.size.y - 0.25)

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
        if self.dragging:
            dx = pos - self.start
            dxd = self.axis.data2inch.mapVector(dx)
            self.axis.set_viewlim(self.axis.view_lim - dxd)
            self.start = pos
            self.bl_paint()
        if self.zooming:
            dx = pos - self.start_zooming
            dxd = -self.axis.data2inch.mapVector(dx)
            self.axis.set_viewlim(self.axis.view_lim * (1+0.2*dxd))
            self.start_zooming = pos
            self.bl_paint()

    def bl_paint(self):
        ci = g.BLContextCreateInfo()
        ci.threadCount = 4
        ctx = Context()
        ctx.begin(self.blImage, ci)
        ctx.setFillStyle(Rgba32(0xFF000000))
        ctx.fillAll()
        ctx.setCompOp(g.BL_COMP_OP_SRC_COPY)
        ctx.setStrokeTransformOrder(g.BL_STROKE_TRANSFORM_ORDER_BEFORE)
        ctx.transform(self.pixel2inch)
        self.axis.draw(ctx)
        ctx.end()

if __name__ == "__main__":
    import numpy as np
    from color import colors
    app = QApplication([])
    c = Canvas()
    x = np.linspace(-10, 10, 2000)
    y = np.sin(x)

    c.show()
    t = QTimer()

    fn = []
    N = 4
    r = np.random.randint(0, len(colors), size=N)
    for i in range(N):
        l = c.axis.add_line(x, y, list(colors)[i], 4)
    c.frames = 0
    c.last_t = c.dt()


    def update_xy(l=l, i=i):
        c.frames += 1
        if c.frames % 60 == 0:
            t = time.time()
            c.setWindowTitle(f"{60 / (t-c.last_t)} fps")
            c.last_t = t

        for i in range(N):
            c.axis.artists[i].y = (np.sin(x+(i+1)*c.dt())*np.sin(x/3+5*c.dt())
                + i/5.11 + np.random.normal(scale=0.05, size=x.size))

        c.repaint()

    t.timeout.connect(update_xy)
    t.start()

app.exec()

