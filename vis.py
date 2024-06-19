#!/usr/bin/env python3

from sys import argv
import numpy as np
from matplotlib import pyplot as plt
import numba
import scipy


@numba.njit
def kart(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z


@numba.njit
def spher(x, y, z):
    r = np.sqrt(x * x + y * y + z * z)
    theta = np.arccos(z / r) if x != 0.0 else 0.0
    phi = np.arctan(y / x) if x != 0.0 else 0.0
    return r, theta, phi


@numba.njit
def factorial(n):
    res = 1
    for i in range(1, n):
        res *= i
    return res

def L(s, t, x):
    def term(j, y):
        sign = ((-1) ** (j + s))
        a = (factorial(t) ** 2) * (x ** j)
        b = factorial(j) * factorial(j + s) * factorial(t - j - s)
        return sign * a * pow(y, j) / b

    res = 0
    for j in range((t - s) + 1):
        res += term(j, x)
    return res

"""
def L(s, t, x):
    res = 0
    for j in range(t):
        sign = ((-1) ** (j + s))
        res += sign * np.random.binomial(s, t) * pow(x, j) / factorial(j)
    return res
"""

def make_sgl(n, l, m):
    def radial(x, y, z):
        r, _, _ = spher(x, y, z)
        #a0 = 5.29e-11
        a0 = 1.0
        a = - np.sqrt(factorial(n - l - 1) / (2 * n * (factorial(n + l) ** 3) ))
        b = (2 / (n * a0)) ** (3.0 / 2.0)
        c = (2 * r / (n * a0)) ** l
        d = np.exp(-r / (n * a0))
        return a * b * c * d * L((2 * l) + 1, n + l, 2 * r / (n * a0))

    def angle(x, y, z):
        _, theta, phi = spher(x, y, z)
        return scipy.special.sph_harm(m, n, theta, phi)

    return lambda x, y, z: angle(x, y, z) * radial(x, y, z)


def make_rsgl(n, l, m):
    def radial(r, theta, phi):
        a0 = 1.0
        a = - np.sqrt(factorial(n - l - 1) / (2 * n * (factorial(n + l) ** 3) ))
        b = (2 / (n * a0)) ** (3.0 / 2.0)
        c = (2 * r / (n * a0)) ** l
        d = np.exp(-r / (n * a0))
        return a * b * c * d * L((2 * l) + 1, n + l, 2 * r / (n * a0))

    def angle(r, theta, phi):
        return scipy.special.sph_harm(m, l, theta, phi)

    return lambda r, theta, phi: angle(r, theta, phi)  * radial(r, theta, phi)


def grid(xrange, yrange, zrange, count):
    res_x = []
    res_y = []
    res_z = []
    delta_x = (xrange[1] - xrange[0]) / count
    delta_y = (yrange[1] - yrange[0]) / count
    delta_z = (zrange[1] - zrange[0]) / count
    for ix in range(count):
        for iy in range(count):
            for iz in range(count):
                res_x.append(xrange[0] + ix * delta_x)
                res_y.append(xrange[0] + iy * delta_y)
                res_z.append(xrange[0] + iz * delta_z)

    return np.array(res_x), np.array(res_y), np.array(res_z)

def grid_2d(xrange, yrange, count):
        res_x = []
        res_y = []
        delta_x = (xrange[1] - xrange[0]) / count
        delta_y = (yrange[1] - yrange[0]) / count
        for ix in range(count):
            for iy in range(count):
                for iz in range(count):
                    res_x.append(xrange[0] + ix * delta_x)
                    res_y.append(xrange[0] + iy * delta_y)

        return np.array(res_x), np.array(res_y)


def max_likelyhood(n, l, m, theta, phi):
    proto_sgl = make_rsgl(n, l, m)
    sgl_lambda = lambda x, a, b: proto_sgl(x, a, b)
    rsgl = np.vectorize(sgl_lambda)
    r = np.linspace(0, 20, 100)
    prob = np.abs(rsgl(r, theta, phi))
    index = np.where(prob == np.max(prob))[-1]
#    print(index)
#    print(prob)
    return r[index]


def not_main():
    n, l, m = int(argv[1]), int(argv[2]), int(argv[3])

    sgl = make_sgl(n, l, m)
    sgl_v = np.vectorize(lambda a, b, c: sgl(a, b, c))

    x, y, z = grid((-70, 70), (-70, 70), (-70, 70), 50)
    density = np.abs(sgl_v(x, y, z)) ** 2


    select = (density > 1e-17) #& (density < 1e-7)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    X, Y = np.meshgrid(x[select], y[select])
    Z = np.reshape(z[select], X.shape)
    ax.plot_surface(X, Y, Z)
    # Set an equal aspect ratio
    ax.set_aspect('equal')

    plt.show()


def main():
    n, l, m = int(argv[1]), int(argv[2]), int(argv[3])

    sgl = make_sgl(n, l, m)
    sgl_v = np.vectorize(lambda a, b: sgl(a, b, 0))

    im = []
    x, y = -25, -25
    while x <= 25:
        im.append([])
        y = -25
        while y <= 25:
            im[-1].append(np.abs(sgl(x, y, 0)) ** 2)
            y += 0.1
        x += 0.1

    im = np.array(im)
    plt.imshow(im)
    plt.show()


def nope():
    n, l, m = int(argv[1]), int(argv[2]), int(argv[3])
    rsgl = make_rsgl(n, l, m)
    print(rsgl(1.0, 1.5, 1.5))

if __name__ == "__main__":
    main()
