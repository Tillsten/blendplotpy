cmake_minimum_required(VERSION 3.20)
project(pyblendplot)
find_package(PythonExtensions REQUIRED)
#add_subdirectory(asmjit)
add_subdirectory(blend2d)
python_extension_module(blend2d)

install(TARGETS blend2d LIBRARY DESTINATION pyblendplot)
