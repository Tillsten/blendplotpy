# blendplot

Very fast toy-plotting library. Uses [Blend2d](https://blend2d.com) for rendering. Out can be displayed
in a QtWidget. Blend2d is build during package creation using scikit-build. Currently uses `cppyy` to interface with blend2d, but this could
be replaced with `pybind11` if necessary. Tested mainly under windows.

![grafik](https://user-images.githubusercontent.com/189880/152532410-4da4eccc-eff2-4735-a9be-33f66bd8d7e0.png)

Run the `example.py` to get an idea. 

Current Features:
* Line Plot
* Scatter Plot
* Panning (middle mouse button) and zooming (right mouse button). Zoom behavior may be buggy.
* Speed
