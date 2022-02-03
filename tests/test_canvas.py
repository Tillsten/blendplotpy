from blendplot.canvas import Canvas
import numpy as np

def test_canvas():
    c = Canvas()
    ax = c.make_axis()
    l = ax.add_line(np.arange(10.0), np.arange(10.0), color='red')
    c.bl_paint()