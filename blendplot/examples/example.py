from qtpy.QtCore import QTimer, Qt, QThread
from qtpy.QtWidgets import QWidget, QApplication
import numpy as np
from blendplot.canvas import Canvas
from blendplot.color import colors
import time

app = QApplication([])
c = Canvas()
x = np.linspace(-10, 10, 1000)
y = np.sin(x)

c.show()
t = QTimer()

fn = []
N = 20
r = np.random.randint(0, len(colors), size=N)
for i in range(N):
    l = c.axis.add_line(x, y, list(colors)[i], 3)
c.frames = 0
c.last_t = c.dt()


def update_xy(l=l, i=i):
    c.frames += 1
    if c.frames % 60 == 0:
        t = time.time()
        c.setWindowTitle(f"{60 / (t-c.last_t): .1f} fps")
        c.last_t = t
    for i in range(N):
        c.axis.artists[i].y = (np.sin(x+(i+1)*c.dt())*np.sin(x/3+5*c.dt())
                               + i/5.11 + np.random.normal(scale=0.05, size=x.size))
    c.repaint()


t.timeout.connect(update_xy)
t.start()
app.exec()
