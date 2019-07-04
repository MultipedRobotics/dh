#!/usr/bin/env python

import numpy as np
from math import sin, cos, tan, pi
import vtk
from test-vtk import vtkWindow

L1 = 52
L2 = 89
L3 = 90
L4 = 95

theta = [-45, 77.41, -98.15, -69.27] # mm
# xyz = (110,-110,-40) mm

params = {
    'units': "degs",
    1: {'a': 0, 'alpha': 0, 'd': 0, 'theta': theta[0]},
    2: {'a': L1, 'alpha': 90, 'd': 0, 'theta': theta[1]},
    3: {'a': L2, 'alpha': 0, 'd': 0, 'theta': theta[2]},
    4: {'a': L3, 'alpha': 0, 'd': 0, 'theta': theta[3]},
    5: {'a': L4, 'alpha': 0, 'd': 0, 'theta': 0}
}

class Mathematics(object):
    def rot2rpy(self, rot):
        return (0,0,0)


class Model(Mathematics):
    def __init__(self):
        self.transform = np.eye(4)
        self.t = []

    def makeT(self, a, alpha, d, theta):
        """
        a - link length from z[i] to z[i+1] along x[i]
        alpha - twist from z[i] to z[i+1] about x[i]
        d - offset from x[i-1] to x[i] along z[i]
        theta - rotation from x[i-1] to x[i] about z[i]

        create a modified DH homogenious matrix (4x4)
        """
        T = np.array([
            [           cos(theta),           -sin(theta),           0,             a],
            [sin(theta)*cos(alpha), cos(theta)*cos(alpha), -sin(alpha), -d*sin(alpha)],
            [sin(theta)*sin(alpha), cos(theta)*sin(alpha),  cos(alpha),  d*cos(alpha)],
            [                    0,                     0,           0,             1]
        ])
        return T

    def create(self, params):
        self.transform = np.eye(4)
        self.t = []

        if 'units' in params:
            units = params.pop('units')
            if units not in ['rads', 'degs']:
                raise Exception("Invalid model units:", units)
        else:
            raise Exception("No units in model parameters")

        for i in sorted(params.keys()):
            print(">>", i)
            m = params[i]

            if units == "degs":
                m['theta'] *= pi/180
                m['alpha'] *= pi/180

            t = self.makeT(m['a'], m['alpha'], m['d'], m['theta'])
            self.t.append(t)
            self.transform = self.transform.dot(t)

    def __str__(self):
        r, p, y = self.rot2rpy(self.transform)
        s = "Translation: {:.1f} {:.1f} {:.1f}  Rotation: {:.2f} {:.2f} {:.2f}".format(
            self.transform[0,3],
            self.transform[1,3],
            self.transform[2,3],
            r, p, y
        )
        return s


m = Model()
m.create(params)
print(m.transform)
print(m)
