# blendplot

Very fast toy-plotting library using blend2d for rendering. Displays in a
QtWidget. Blend2d is build during package creation using scikit-build.
Currently uses `cppyy` to interface with blend2d, but this could
be replaced with `pybind11` if necessary. Building is only tested under windows
and may be still buggy. 

Currenty only displays lines. Zooming behavior is also still buggy.


