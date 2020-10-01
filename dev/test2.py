#!/usr/bin/env python3

"""Basic usage of the pybotics package."""
import numpy as np
from mdh import __version__ as version
from mdh.link import mdh_params, JointType, RevoluteLink
from mdh.kinematic_chain import KinematicChain

pi = np.pi

print(f">> {version}")

# make it print better
np.set_printoptions(suppress=True)

def kevin():
    mm = pi
    """alpha a theta d"""
    dh = [
        {'alpha':    0, 'a':  0, 'theta': 0, 'd': 0, 'type': 1},
        {'alpha': pi/2, 'a': 50, 'theta': 0, 'd': 0, 'type': 1},
        {'alpha':    0, 'a': 65, 'theta': 0, 'd': 0, 'type': 1},
        {'alpha': 0, 'a': 68, 'theta': 0, 'd': 0, 'type': 1, 'fixed': True}
    ]

    return dh

def main():
    # l = RevoluteLink(1,2,3,4)

    t = kevin()
    kc = KinematicChain.from_parameters(t)
    print(f">> size: {kc.size}")

    for l in kc:
        print(f">> {l}")

    t = kc.forward(np.deg2rad([0,0,0,0]))
    print(t)

    t = kc.forward(np.deg2rad([0,82.62,-154.1,0]))
    print(t)

    jnts = kc.inverse(t)
    print(">> ", np.rad2deg(jnts))

    p = np.array([
        [0,1,0, 80],
        [0,0,-1,0],
        [-1,0,0,0],
        [0,0,0,1]
    ])

    # p = np.array([
    #     [1,0,0, 80],
    #     [0,1,0,0],
    #     [0,0,1,0],
    #     [0,0,0,1]
    # ])

    jnts = kc.inverse(p)
    print(">> ", np.rad2deg(jnts))

if __name__ == "__main__":
    main()
