import numpy as np


def get_ticks(minmax, size):
    print(size//4)
    return np.linspace(minmax[0], minmax[1], int(3*size))
