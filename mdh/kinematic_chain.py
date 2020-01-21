import numpy as np # type: ignore
import attr
from typing import Any, Optional, Sequence, Sized, Union, Iterable, Dict, List
import scipy # type: ignore
import scipy.optimize # type: ignore
# from numpy.linalg import norm
from collections import namedtuple
from mdh.link import mdh_params, RevoluteLink, JointType
from scipy.spatial.transform import Rotation as R # type: ignore
from math import atan2, pi

"""

"""

# Pose = namedtuple('Pose', "position rotation")

@attr.s
class KinematicChain(Sized, Iterable):
    _links = attr.ib(type=Sequence[Any])

    def __len__(self):
        return len(self._links)

    def __iter__(self):
        for l in self._links:
            yield l

    def transform(self, joints: Sequence[float]):
        """Calculates the transformation and returns a 4x4 matrix"""
        if len(joints) != len(self._links):
            raise Exception("inputs don't equal number of links")

        t = np.eye(4)
        for l, q in zip(reversed(self._links), reversed(joints)):
            m = l.transform(q)
            t = m.dot(t)
            # t = m @ t
            # t = np.dot(m, t)
        return t

    def forward(self, joints: Sequence[float]):
        """value?
        Solve the forward kinematics and returns a 4x4 matrix
        """
        return self.transform(joints)

    def inverse(self, pos: Sequence[float]) -> Optional[np.ndarray]:
            """
            Solve the inverse kinematics and returns 1xN on success or None
            on failure.

            FIXME: this only works for when the foot is straight down
            """
            j = [[],[]] # type: Sequence[List]
            for l in self:
                j[0].append(l.min)
                j[1].append(l.max)
            j[0][4] = -0.00001
            j[1][4] = 0.00001

            joint_limits = np.array(j) # type: np.ndarray
            # print(joint_limits)

            # r = R.from_matrix([[1,0,0],[0,0,-1],[0,1,0]])
            # rr = R.from_euler('z', atan2(pos[1], pos[0]))
            # c = rr*r

            # make desired transform pose (position, oritentation)
            # change the -90 x-axis to something else for non-down??
            x = pos[0]
            y = pos[1]
            c = R.from_euler('zyx', [-90,atan2(y,x)*180/pi,90], degrees=True)
            ppos = np.eye(4)
            ppos[:3,:3] = c.as_matrix()
            ppos[:3, 3] = pos

            start = [0]*len(self._links)

            result = scipy.optimize.least_squares(
                fun=_ik_cost_function,
                x0=np.array(start),
                bounds=joint_limits,
                args=(ppos, self)
            )  # type: scipy.optimize.OptimizeResult

            if result.success:  # pragma: no cover
                # print(">> yeah!!!")
                # print(">>", np.rad2deg(result.x))
                actual_t = self.transform(result.x)
                actual_pos = actual_t[:3,3]
                if np.allclose(actual_pos, pos, atol=1e-3):
                    return result.x
            return None

    @classmethod
    def from_parameters(cls: Any, params: Union[Sequence[Dict], Sequence[mdh_params]]):
        """Builds a KinematicChain object from an input"""
        links = []
        for l in params:
            if isinstance(l, dict):
                l = mdh_params(l['alpha'], l['a'], l['theta'], l['d'], l['type'])
            # print(f">> {l}")
            if l.type == JointType.revolute:
                link = RevoluteLink(a=l.a, alpha=l.alpha, d=l.d, theta=l.theta)
                # print(link.transform(0),'\n')
                links.append(link)
            elif l.type == JointType.prismatic:
                raise NotImplementedError(f"from_parameters: {l.type}")
            else:
                raise Exception(f"Invalid parameter: {l.type}")

        ret = cls(links)

        return ret

def _ik_cost_function(ik_q: np.ndarray, pose: np.ndarray, kc: KinematicChain) -> np.ndarray:
    """Cost function for least squares algorithm.
        - ik_q: calculated 4x4 matrix from optimization
        - pose: desired 4x4 matrix with position and orientation
        - kc: KinematicChain object that is trying to find this info
    """
    actual_t = kc.transform(ik_q)
    diff = np.abs(actual_t - pose)
    return diff.ravel()
