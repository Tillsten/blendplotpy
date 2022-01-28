cmake_minimum_required(VERSION 3.22)
project(blendplotpy)

#add_subdirectory(asmjit)
add_subdirectory(blend2d)
python_extension_module(blend2d)
install(TARGETS blend2d LIBRARY DESTINATION blendplotpy)

