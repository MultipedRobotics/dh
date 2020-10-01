import numpy as np # type: ignore
import attr
# from typing import Any, Optional, Sequence, Sized, Union, Iterable, Dict, List
# import scipy # type: ignore
import scipy.optimize # type: ignore
# from numpy.linalg import norm
from collections import namedtuple
from mdh.link import mdh_params
from mdh.link import RevoluteLink
from mdh.link import JointType
from scipy.spatial.transform import Rotation as R # type: ignore
from math import atan2, pi

"""

"""

# Pose = namedtuple('Pose', "position rotation")

class UnReachable(Exception):
    pass

@attr.s
# class KinematicChain(Sized, Iterable):
class KinematicChain:
    # _links = attr.ib(type=Sequence[Any])
    _links = attr.ib()
    _size = attr.ib()

    def __len__(self):
        """Enables the length function, returns number links"""
        # return len(self._links)
        return self._size

    def __iter__(self):
        """Enables iteration of joints:  for j in chain: print(j)"""
        for l in self._links:
            yield l

    def __getitem__(self, key):
        """Return a link"""
        return self._links[key]

    def transform(self, joints):
        """Calculates the transformation and returns a 4x4 matrix"""
        if len(joints) != self.size:
            raise Exception(f"inputs don't equal number of links {len(joints)} != {self.size}")

        t = np.eye(4)
        for l, q in zip(reversed(self._links), reversed(joints)):
            m = l.transform(q)
            t = m.dot(t)
        return t

    def forward(self, joints):
        """value?
        Solve the forward kinematics and returns a 4x4 matrix

        return: (position), (euler angles)
        """
        return self.transform(joints)

    def inverse(self, pos):
            """
            Solve the inverse kinematics and returns 1xN on success or None
            on failure.

            FIXME: this only works for when the foot is straight down
            """
            joint_limits = [[],[]] # type: Sequence[List]
            for l in self:
                joint_limits[0].append(l.min)
                joint_limits[1].append(l.max)
            # # j[0][3] = -0.00001
            # # j[1][3] = 0.00001
            # joint_limits = j
            # joint_limits = np.array(j) # type: np.ndarray
            # print(joint_limits)

            # r = R.from_matrix([[1,0,0],[0,0,-1],[0,1,0]])
            # rr = R.from_euler('z', atan2(pos[1], pos[0]))
            # c = rr*r

            # make desired transform pose (position, oritentation)
            # change the -90 x-axis to something else for non-down??
            # x = pos[0]
            # y = pos[1]
            # c = R.from_euler('zyx', [-90,atan2(y,x)*180/pi,90], degrees=True)
            # ppos = np.eye(4)
            # ppos[:3,:3] = c.as_matrix()
            # ppos[:3, 3] = pos

            start = [0]*len(self._links)

            result = scipy.optimize.least_squares(
                fun=_ik_cost_function,
                x0=np.array(start),
                bounds=joint_limits,
                args=(pos, self)
            )

            if not result.success:  # pragma: no cover
                raise UnReachable(f"Can't reach: {pos}m")
            # print(">> yeah!!!")
            # print(">>", np.rad2deg(result.x))
            actual_t = self.transform(result.x)
            actual_pos = actual_t #actual_t[:3,3]
            if np.allclose(actual_pos, pos, atol=1e-3):
                # print(result)
                return result.x

            raise UnReachable(f"Can't reach: {pos}")

    @property
    def size(self):
        return self._size

    @classmethod
    def from_parameters(cls, params):
        """Builds a KinematicChain object from an input"""
        links = []
        size = 0
        for l in params:
            if not isinstance(l, dict):
                raise Exception(f"Invalid parameters: {l}")

            for key in ['alpha', 'a', 'theta', 'd']:
                if key not in l:
                    raise Exception(f"Missing parameter: {key}")

            # ll = mdh_params(l['alpha'], l['a'], l['theta'], l['d'])
            # print(f">> params: {ll}")
            # print(l['alpha'])

            # if ll.type == JointType.revolute:
            # link = RevoluteLink(a=ll.a, alpha=ll.alpha, d=ll.d, theta=ll.theta)
            # link = RevoluteLink(alpha=ll.alpha, a=ll.a, theta=ll.theta, d=ll.d)
            link = RevoluteLink(l['alpha'], l['a'], l['theta'], l['d'])
            # elif ll.type == JointType.prismatic:
            #     raise NotImplementedError(f"from_parameters: {l.type}")
            # else:
            #     raise Exception(f"Invalid parameter: {l.type}")

            # if "max_min" in l:
            #     link.min = l["max_min"][1]
            #     link.max = l["max_min"][0]
            # else:
            link.min = -pi
            link.max = pi

            links.append(link)

            # if 'fixed' in l:
            #     if l['fixed'] is not True:
            #         size += 1
            # else:
            #     size += 1
            size += 1

        ret = cls(links, size)

        return ret

def _ik_cost_function(ik_q, pose, kc):
    """Cost function for least squares algorithm.
        - ik_q: calculated 4x4 matrix from optimization
        - pose: desired 4x4 matrix with position and orientation
        - kc: KinematicChain object that is trying to find this info
    """
    actual_t = kc.transform(ik_q)
    diff = np.abs(actual_t - pose)
    return diff.ravel()
