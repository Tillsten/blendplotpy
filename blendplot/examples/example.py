from qtpy.QtCore import QTimer, Qt, QThread
from qtpy.QtWidgets import QWidget, QApplication
import numpy as np
from blendplot.artists import Scatter
from blendplot.canvas import CanvasQT
from blendplot.color import colors
from blendplot.blendpy import Box, Rgba32
import time

app = QApplication([])
c = CanvasQT()
ax = c.make_axis()
x = np.linspace(-10, 10, 1000)
y = np.sin(x)

c.show()
t = QTimer()

fn = []
N = 5
r = np.random.randint(0, len(colors), size=N)
for i in range(N):
    lc = list(colors)[r[i]]
    lc = Rgba32(colors[lc])
    lc.setA(128)
    l = ax.add_line(x, y, lc, 8)


r = np.random.randint(0, len(Scatter.symbols_list), size=N)
for i in range(N):
    lc = list(colors)[r[i]]
    lc = Rgba32(colors[lc])
    lc.setA(128)
    s = list(Scatter.symbols_list)[r[i]]
    l = Scatter(x[::4], y[::4], lc, colors['white'], symbol=s, size=8)
    ax.add_artist(l)
r = np.random.multivariate_normal([2, 2], np.eye(2), 1000)

c.frames = 0
c.last_t = c.dt()
ax.set_viewlim(Box(-10, -2, 10, 7))

def update_xy(l=l, i=i):
    c.frames += 1
    if c.frames % 60 == 0:
        t = time.time()
        c.setWindowTitle(f"{60 / (t-c.last_t): .1f} fps")
        c.last_t = t
    for i in range(2*N):
        y = (np.sin(x+(i/3+1)*c.dt())*np.sin(x/3+1*c.dt())
             + i/4.11 + np.random.normal(scale=0.05, size=x.size))
        if i <= N:
            ax.artists[i].set_data(x, y)
        else:
            ax.artists[i].set_data(x[::10], y[::10])

    c.repaint()


t.timeout.connect(update_xy)
t.start()
app.exec()