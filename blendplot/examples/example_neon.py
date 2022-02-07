from qtpy.QtCore import QTimer, Qt, QThread
from qtpy.QtWidgets import QWidget, QApplication
import numpy as np
from blendplot.canvas import CanvasQT
from blendplot.color import colors
from blendplot.blendpy import Box, Rgba32
import time

app = QApplication([])
c = CanvasQT()
ax = c.make_axis()
x = np.linspace(-10, 10, 1280)
y = np.sin(x)

c.show()
t = QTimer()

fn = []
N = 10

for i in range(N):

    lc = Rgba32(colors["bright pink"])
    lc.setA(10)
    l = ax.add_line(x, y, lc, 5+1*(i**2))
c.frames = 0
c.last_t = c.dt()
ax.set_viewlim(Box(-10, -2, 10, 7))

def update_xy(l=l, i=i):
    c.frames += 1
    if c.frames % 60 == 0:
        t = time.time()
        c.setWindowTitle(f"{60 / (t-c.last_t): .1f} fps")
        c.last_t = t
    for i in range(N):
        y = (np.sin(x+(3+1)*c.dt())*np.sin(x/3+1*c.dt())
             + 4.11 )
        ax.artists[i].set_data(x, y)

    c.repaint()


t.timeout.connect(update_xy)
t.start()
app.exec()
