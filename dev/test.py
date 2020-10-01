#!/usr/bin/env python

"""Basic usage of the pybotics package."""
import numpy as np
from mdh import __version__ as version
from mdh.link import mdh_params, JointType
from mdh.kinematic_chain import KinematicChain

pi = np.pi

print(f">> {version}")

# make it print better
np.set_printoptions(suppress=True)

def kevin():
    mm = pi
    """alpha a theta d"""
    dh = [
        {'alpha':    0, 'a':  0, 'theta': 0, 'd': 0, 'type': 1, "max_min": [mm,-mm]},
        {'alpha': pi/2, 'a': 52, 'theta': 0, 'd': 0, 'type': 1, "max_min": [mm,-mm]},
        {'alpha':    0, 'a': 89, 'theta': 0, 'd': 0, 'type': 1, "max_min": [mm,-mm]},
        {'alpha':    0, 'a': 90, 'theta': 0, 'd': 0, 'type': 1, "max_min": [mm,-mm]},
        {'alpha':    0, 'a': 95, 'theta': 0, 'd': 0, 'type': 1, "max_min": [mm,-mm]}
    ]

    return dh

def main():

    t = kevin()
    kc = KinematicChain.from_parameters(t)

    # j = [
    #     [0,0,0,0,0],
    #     [0,pi/4,-pi/4,-pi/2,0], # 204, 0, -32
    #     # [0,0,-pi/2,0,0],
    #     # np.deg2rad([90,131.17,-106.19,-114.98]),
    #     np.deg2rad([-45.00, 77.41, -98.15, -69.27, 0]) # 110, -110, -40
    # ]

    # for jj in j:
    #     # print(jj)
    #     t = kc.transform(jj)
    #     print(t)
    #     print("----------------------")

    j = [
        [204.93, 0, -32.067],
        [110,-110,-40],
        [110,110,-40],
        [110,0,-70]
    ]

    for jj in j:
        p = np.array([
            [0,1,0, jj[0]],
            [0,0,-1,jj[1]],
            [-1,0,0,jj[2]],
            [0,0,0,1]
        ])
        rads = kc.inverse(p)
        print(">>", np.rad2deg(rads))


if __name__ == "__main__":
    main()
