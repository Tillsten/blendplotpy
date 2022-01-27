from pathlib import Path
import cppyy
import time
import cppyy.gbl as g

cppyy.add_include_path(str(Path(__file__).parent / 'include'))
cppyy.include('blend2d.h')
cppyy.load_library('blend2d.dll')

cppyy.cppdef("""
#include <vector>
void make_path(const std::vector<float>& x, const std::vector<float>& y, BLPath& p)
 {
     int n = x.size();
     p.reserve(n+10);
     p.moveTo(x[0], y[0]);
     for (int i = 1; i<n;i++) {
         p.lineTo(x[i], y[i]);
     };
 }
""")

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

g.BLContext.strokePath.__release_gil__ = True
Context = g.BLContext

Image = g.BLImage

g.BLRgba32.__str__ = lambda p: 'Rgba32(r=%d, g=%d, b=%d, a=%d)' % (p.r, p.g, p.b, p.a)
Rgba32 = g.BLRgba32

face = g.BLFontFace()
err = face.createFromFile("NotoSans-Regular.ttf")
font = g.BLFont()
font.createFromFace(face, 15)

