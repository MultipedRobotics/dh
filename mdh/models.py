# MIT Licensed


import numpy as np
from collections import namedtuple

RobotModel = namedtuple('RobotModel', "dh angles")

def kuka_lbr_iiwa_7():
    """Get KUKA LBR iiwa 7 MDH model. (https://github.com/nnadeau/pybotics)"""
    dh = [
        {'alpha':          0, 'theta': 0, 'd': 0, 'a': 0.340},
        {'alpha': -np.pi / 2, 'theta': 0, 'd': 0, 'a': 0},
        {'alpha':  np.pi / 2, 'theta': 0, 'd': 0, 'a': 0.400},
        {'alpha':  np.pi / 2, 'theta': 0, 'd': 0, 'a': 0},
        {'alpha': -np.pi / 2, 'theta': 0, 'd': 0, 'a': 0.400},
        {'alpha': -np.pi / 2, 'theta': 0, 'd': 0, 'a': 0},
        {'alpha':  np.pi / 2, 'theta': 0, 'd': 0, 'a': 0.126},
    ]
    return dh

def kuka_kr_500():
    """KUKA KR 500 (Forces Acting on the Robot during Grinding, Thesis, Adam Tresnak, 2017)"""
    dh = [
        {'alpha':  np.pi / 2, 'theta': 0, 'd': -1.045, 'a': 0.5},
        {'alpha':          0, 'theta': 0, 'd':      0, 'a': 1.3},
        {'alpha': -np.pi / 2, 'theta': 0, 'd':      0, 'a': 0.055},
        {'alpha':  np.pi / 2, 'theta': 0, 'd': -1.025, 'a': 0},
        {'alpha': -np.pi / 2, 'theta': 0, 'd':      0, 'a': 0},
        {'alpha':      np.pi, 'theta': 0, 'd': -0.290, 'a': 0},
    ]
    return dh

# def mecademic_meca500():
#     """Get Meca500 MDH model."""
#     return np.array(
#         {
#             {0, 0, 0, 135},
#             {-np.pi / 2, 0, -np.pi / 2, 0},
#             {0, 135, 0, 0},
#             {-np.pi / 2, 38, 0, 120},
#             {np.pi / 2, 0, 0, 0},
#             {-np.pi / 2, 0, np.pi, 72},
#         }
#     )
#
#
def puma560():
    """Get PUMA560 MDH model."""
    return [
            {'alpha':          0, 'a':     0, 'theta':     0, 'd': 0},
            {'alpha': -np.pi / 2, 'a':     0, 'theta':     0, 'd': 0},
            {'alpha':          0, 'a': 612.7, 'theta':     0, 'd': 0},
            {'alpha':          0, 'a': 571.6, 'theta':     0, 'd': 163.9},
            {'alpha': -np.pi / 2, 'a':     0, 'theta':     0, 'd': 115.7},
            {'alpha':  np.pi / 2, 'a':     0, 'theta': np.pi, 'd': 92.2},
        ]
#
#
# def ur10():
#     """Get UR10 MDH model."""
#     return np.array(
#         {
#             {0, 0, 0, 118},
#             {np.pi / 2, 0, np.pi, 0},
#             {0, 612.7, 0, 0},
#             {0, 571.6, 0, 163.9},
#             {-np.pi / 2, 0, 0, 115.7},
#             {np.pi / 2, 0, np.pi, 92.2},
#         }
#     )
