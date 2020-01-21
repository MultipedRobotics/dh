# import numpy as np # type: ignore
# import attr
# from typing import Any, Optional, Sequence, Sized, Union, Iterable
# # import scipy
# # import scipy.optimize
# # from numpy.linalg import norm
# # from collections import namedtuple
# # from mdh.link import mdh_params, RevoluteLink, JointType
# # from scipy.spatial.transform import Rotation as R
# # from math import atan2, pi
# from mdh.kinematic_chain import KinematicChain
#
# @attr.s
# class Leg(KinematicChain):
#     """
#     inherets fk/ik, read/write json
#     has:
#         - foot position, orientation [m, quaternion???]
#         - joint angles [rads]
#     """
#     foot = attr.ib(type=Sequence[float])
#
#     # @property
#     # def
