from pathlib import Path
import cppyy
import cppyy.gbl as g


cur_dir = Path(__file__).parent


cppyy.add_include_path(str(cur_dir / 'include'))
cppyy.include('blend2d.h')
cppyy.load_library(str(cur_dir/ 'bin/blend2d.dll'))

print(__file__)
cppyy.cppdef((cur_dir/"cpp_helpers.cpp").open().read())


get_ticks = g.calculate_ticks
make_path = g.make_path

def m_print(m):
    s = ''
    for i in range(3):
        for j in range(2):
            s += '%.2f ' % getattr(m, 'm%d%d' % (i, j))
    return s
g.BLMatrix2D.__str__ = m_print
Matrix2D = g.BLMatrix2D

g.BLPoint.__str__ = lambda p: 'Point(x=%.2f, y=%.2f)' % (p.x, p.y)
Point = g.BLPoint

g.BLBox.__str__ = lambda p: 'Box(x0=%.2f, y0=%.2f, x1=%.2f, y1=%.2f)' % (
    p.x0, p.y0, p.x1, p.y1)
Box = g.BLBox

g.BLRect.__str__ = lambda p: 'Box(x0=%.2f, y0=%.2f, w=%.2f, h=%.2f)' % (
    p.x0, p.y0, p.w, p.h)
Rect = g.BLRect

g.BLContext.strokePath.__release_gil__ = True
g.BLContext.end.__release_gil__ = True
Context = g.BLContext

Image = g.BLImage

g.BLRgba32.__str__ = lambda p: 'Rgba32(r=%d, g=%d, b=%d, a=%d)' % (p.r, p.g, p.b, p.a)
Rgba32 = g.BLRgba32

face = g.BLFontFace()
err = face.createFromFile("NotoSans-Regular.ttf")
font = g.BLFont()
font.createFromFace(face, 1/72*8)

