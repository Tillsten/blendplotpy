from qtpy.QtCore import QTimer, Qt, QThread
from qtpy.QtWidgets import QWidget, QApplication
import numpy as np
from blendplot.canvas import CanvasQT
from blendplot.color import colors
from blendplot.blendpy import Box, Rgba32
from blendplot.artists import Scatter
import time

app = QApplication([])
c = CanvasQT()
ax = c.make_axis()
c.show()
c.frames = 0
c.last_t = c.dt()
t = QTimer()

fn = []
N = 3
x = np.array([1])
y = np.array([1])

color = Rgba32(colors["orange"])
color.setA(2)
color2 = Rgba32(colors["orange"])
color2.setA(2)
l = Scatter(x, y, color, color2, size=25, symbol='s')
ax.add_artist(l)
   

ax.set_viewlim(Box(-5, -5, 5, 5))

def update_xy(l=l):
    global x
    global y
    c.frames += 1
    if c.frames % 5 == 0:
        t = time.time()
        c.setWindowTitle(f"{60 / (t-c.last_t): .1f} fps, {x.size} points")
        c.last_t = t        
    
        x = np.hstack((x, np.random.randn(15)))
        y = np.hstack((y, np.random.randn(15)))
        l.set_data(x, y)

    c.repaint()


t.timeout.connect(update_xy)
t.start()
app.exec()
