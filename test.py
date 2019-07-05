#!/usr/bin/env python

import numpy as np
from math import sin, cos, tan, pi
import vtk
from test_vtk import vtkWindow, Revolute, n2v

L1 = 52
L2 = 89
L3 = 90
L4 = 95

theta = [-45, 77.41, -98.15, -69.27] # mm
# xyz = (110,-110,-40) mm

params = {
    'units': "degs",
    1: {'a':  0, 'alpha':  0, 'd': 0, 'theta': theta[0]},
    2: {'a': L1, 'alpha': 90, 'd': 0, 'theta': theta[1]},
    3: {'a': L2, 'alpha':  0, 'd': 0, 'theta': theta[2]},
    4: {'a': L3, 'alpha':  0, 'd': 0, 'theta': theta[3]},
    5: {'a': L4, 'alpha':  0, 'd': 0, 'theta': 0}
}


class Mathematics(object):
    def rot2rpy(self, rot):
        return (0, 0, 0)


class Kinematics(Mathematics):
    transform = np.eye(4)  # overall, base to effector transform
    # t = [] # transform for each link from base (useful for display)
    #
    # def __init__(self):
    #     self.transform = np.eye(4)
    #     self.t = []

    def __makeT(self, a, alpha, d, theta):
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

    def add_link(self, a, alpha, d, theta, degs=False):
        if degs:
            alpha *= pi/180
            theta *= pi/180
        t = self.__makeT(a, alpha, d, theta)
        self.transform = self.transform.dot(t)
    #     self.transform = np.eye(4)
    #     self.t = []
    #
    #     if 'units' in params:
    #         units = params.pop('units')
    #         if units not in ['rads', 'degs']:
    #             raise Exception("Invalid model units:", units)
    #     else:
    #         raise Exception("No units in model parameters")
    #
    #     for i in sorted(params.keys()):
    #         print(">>", i)
    #         m = params[i]
    #
    #         if units == "degs":
    #             m['theta'] *= pi/180
    #             m['alpha'] *= pi/180
    #
    #         t = self.makeT(m['a'], m['alpha'], m['d'], m['theta'])
    #         self.transform = self.transform.dot(t)
    #         self.t.append(np.copy(self.transform))

    def str(self, t):
        pass

    def __str__(self):
        r, p, y = self.rot2rpy(self.transform)
        s = "Translation: {:.1f} {:.1f} {:.1f}  Rotation: {:.2f} {:.2f} {:.2f}".format(
            self.transform[0, 3],
            self.transform[1, 3],
            self.transform[2, 3],
            r, p, y
        )
        return s


class Model():
    # def __init__(self):
    #     self.kine = Kinematics()
    #     self.links = []

    def build(self, params):
        # self.transform = np.eye(4)
        self.links = []
        self.actors = []
        self.kine = Kinematics()

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

            self.kine.add_link(m['a'], m['alpha'], m['d'], m['theta'])
            # self.t.append(np.copy(self.kine.transform))

            # there doesn't seem to be a better way to do this
            # t = vtk.vtkTransform()
            # for i in range(4):
            #     for j in range(4):
            #         t[i,j] = self.kine.transform[i,j]

            t = n2v(self.kine.transform)
            rev = Revolute(m['a'],0.5, t)
            self.actors.append(rev)



m = Model()
m.build(params)
# print(m.transform)
# print(m)
