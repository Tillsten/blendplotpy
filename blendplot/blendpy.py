from pathlib import Path
import cppyy
import cppyy.gbl as g


cur_dir = Path(__file__).parent


cppyy.add_include_path(str(cur_dir / 'include'))
if (cur_dir/'lib').exists():
    cppyy.add_library_path(str(cur_dir/'lib')) # linux
if (cur_dir/'bin').exists():
    cppyy.add_library_path(str(cur_dir/'bin')) # windows
cppyy.include('blend2d.h')

cppyy.load_library('blend2d')


cppyy.cppdef((cur_dir/"cpp_helpers.cpp").open().read())


get_ticks = g.calculate_ticks
make_path = g.make_path
draw_scatter = g.draw_scatter
box_union = g.box_union

# Pythonize some of the more often used classes with nicer __str__

def m_print(m):
    s = ''
    for i in range(3):
        for j in range(2):
            s += 'm%d%d=%.2f, ' % (i, j, getattr(m, 'm%d%d' % (i, j)))
    return f'Matrix2D({s})'
g.BLMatrix2D.__str__ = m_print
Matrix2D = g.BLMatrix2D

g.BLPoint.__str__ = lambda p: 'Point(x=%.2f, y=%.2f)' % (p.x, p.y)
Point = g.BLPoint
Point.__repr__ = Point.__str__

g.BLBox.__str__ = lambda p: 'Box(x0=%.2f, y0=%.2f, x1=%.2f, y1=%.2f)' % (
    p.x0, p.y0, p.x1, p.y1)
Box = g.BLBox

g.BLRect.__str__ = lambda p: 'Box(x0=%.2f, y0=%.2f, w=%.2f, h=%.2f)' % (
    p.x0, p.y0, p.w, p.h)
Rect = g.BLRect

#g.BLContext.strokePath.__release_gil__ = True
#g.BLContext.end.__release_gil__ = True
Context = g.BLContext

Image = g.BLImage

g.BLRgba32.__str__ = lambda p: 'Rgba32(r=%d, g=%d, b=%d, a=%d)' % (p.r, p.g, p.b, p.a)
Rgba32 = g.BLRgba32

face = g.BLFontFace()
err = face.createFromFile("NotoSans-Regular.ttf")
font = g.BLFont()
font.createFromFace(face, 1/72*8)

