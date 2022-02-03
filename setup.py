import sys
from skbuild import setup

setup(
    name="blendplot",
    version="0.0.1",
    description="Fast toy-plotting libary based on Blend2d",
    author='Till Stensitzki',
    license="MIT",
    packages=['blendplot'],
    tests_require=['pytest'],
    cmake_source_dir='3rdparty',
    cmake_install_dir='blendplot'
)
