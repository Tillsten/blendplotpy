# blendplot

Very fast toy-plotting library. Uses [Blend2d](https://blend2d.com) for rendering, hence it does not requieres a GPU. 
Output can be displayed in a QtWidget. Blend2d is build during package creation using scikit-build. 
Currently uses `cppyy` to interface with blend2d, but this could be replaced with `pybind11` if necessary. 
Tested mainly under windows.

The figure below shows a scene with 5 line plot each containing 1280 points and a linewidth of 8 in
addition to 5 scatter plot with 128 points each. FPS is still well above 200 ftps.

![grafik](https://user-images.githubusercontent.com/189880/152532410-4da4eccc-eff2-4735-a9be-33f66bd8d7e0.png)

Run the `example.py` to get an idea. 

Current Features:
* Line Plot
* Scatter Plot
* Panning (middle mouse button) and zooming (right mouse button). Zoom behavior may be buggy.
* Speed
