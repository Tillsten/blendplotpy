import sys

from skbuild import setup


setup(
    name="pyblendplot",
    version="0.0.1",
    description="Fast plotting based on Blend2d",
    author='Till Stensitzki',
    license="MIT",
    packages=['pyblendplot'],
    tests_require=['pytest'],
)
