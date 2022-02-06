import numpy as np
from numba import njit

# The tick code is taken from the vispy project and adapted to use numba.


@njit
def _coverage(dmin, dmax, lmin, lmax):
    return 1 - 0.5 * ((dmax - lmax) ** 2 +
                      (dmin - lmin) ** 2) / (0.1 * (dmax - dmin)) ** 2


@njit
def _coverage_max(dmin, dmax, span):
    range_ = dmax - dmin
    if span <= range_:
        return 1.
    else:
        half = (span - range_) / 2.0
        return 1 - half ** 2 / (0.1 * range_) ** 2


@njit
def _density(k, m, dmin, dmax, lmin, lmax):
    r = (k-1.0) / (lmax-lmin)
    rt = (m-1.0) / (max(lmax, dmax) - min(lmin, dmin))
    return 2 - max(r / rt, rt / r)


@njit
def _density_max(k, m):
    return 2 - (k-1.0) / (m-1.0) if k >= m else 1.


@njit
def _simplicity(q, Q, j, lmin, lmax, lstep):
    eps = 1e-10
    n = len(Q)
    i = Q.index(q) + 1
    if ((lmin % lstep) < eps or
            (lstep - lmin % lstep) < eps) and lmin <= 0 and lmax >= 0:
        v = 1
    else:
        v = 0
    return (n - i) / (n - 1.0) + v - j


@njit
def _simplicity_max(q, Q, j):
    n = len(Q)
    i = Q.index(q) + 1
    return (n - i)/(n - 1.0) + 1. - j


@njit
def get_ticks_talbot(dmin, dmax, n_inches, density=1):
    # density * size gives target number of intervals,
    # density * size + 1 gives target number of tick marks,
    # the density function converts this back to a density in data units
    # (not inches)

    n_inches = max(3*n_inches, 2.0)  # Set minimum otherwise code can crash :(
    
    if dmin == dmax:
        return np.array([dmin, dmax])

    m = density * n_inches + 1.0
    only_inside = True  # we cull values outside ourselves
    Q = [1., 5., 2., 2.5, 4., 3.]
    w = [0.25, 0.2, 0.5, 0.05]
    best_score = -2.0
    best = None

    j = 1.0
    n_max = 1000
    while j < n_max:
        for q in Q:
            sm = _simplicity_max(q, Q, j)

            if w[0] * sm + w[1] + w[2] + w[3] < best_score:
                j = n_max
                break

            k = 2.0
            while k < n_max:
                dm = _density_max(k, n_inches)

                if w[0] * sm + w[1] + w[2] * dm + w[3] < best_score:
                    break

                delta = (dmax-dmin)/(k+1.0)/j/q
                z = np.ceil(np.log10(delta))

                while z < np.inf:
                    step = j * q * 10 ** z
                    cm = _coverage_max(dmin, dmax, step*(k-1.0))

                    if (w[0] * sm +
                            w[1] * cm +
                            w[2] * dm +
                            w[3] < best_score):
                        break

                    min_start = np.floor(dmax/step)*j - (k-1.0)*j
                    max_start = np.ceil(dmin/step)*j

                    if min_start > max_start:
                        z = z+1
                        break

                    for start in range(int(min_start), int(max_start)+1):
                        lmin = start * (step/j)
                        lmax = lmin + step*(k-1.0)
                        lstep = step

                        s = _simplicity(q, Q, j, lmin, lmax, lstep)
                        c = _coverage(dmin, dmax, lmin, lmax)
                        d = _density(k, m, dmin, dmax, lmin, lmax)
                        leg = 1.  # _legibility(lmin, lmax, lstep)

                        score = w[0] * s + w[1] * c + w[2] * d + w[3] * leg

                        if (score > best_score and
                                (not only_inside or (lmin >= dmin and
                                                     lmax <= dmax))):
                            best_score = score
                            best = (lmin, lmax, lstep, q, k)
                    z += 1
                k += 1
            if k == n_max:
                raise RuntimeError('could not converge on ticks')
        j += 1
    if j == n_max:
        raise RuntimeError('could not converge on ticks')

    if best is None:
        raise RuntimeError('could not converge on ticks')
    return np.arange(k) * lstep + lmin




