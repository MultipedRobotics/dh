import attr
from collections import namedtuple
from enum import IntFlag
import numpy as np # type: ignore

JointType =  IntFlag('JointType', 'revolute prismatic revolute_theda revolute_alpha')
mdh_params = namedtuple("mdh_params", "alpha a theta d type")

@attr.s
class Link:
    """
    why? what is the value of this?
    prismatic/revolute have parameters that never chance ... need to freeze them!
    """
    # alpha = attr.ib(type=float)
    # a = attr.ib(type=float)
    # theta = attr.ib(type=float)
    # d = attr.ib(type=float)

@attr.s
class RevoluteLink(Link):
    """
    RevoluteLink about theta. All other parameters (alpha, a, d) are fixed and
    cannot be changed once the link is created.
    """
    _alpha = attr.ib(type=float)
    _a = attr.ib(type=float)
    theta = attr.ib(type=float)
    _d = attr.ib(type=float)

    @property
    def alpha(self) -> float:
        return self._alpha

    @property
    def a(self) -> float:
        return self._a

    @property
    def d(self) -> float:
        return self._d

    # max/min limits of link for optimzation
    min = attr.ib(-np.pi, type=float)
    max = attr.ib(np.pi, type=float)

    """Some of these params are immutable, how do I do that?"""
    def transform(self, angle: float):
        """could move this to link"""

        crx = np.cos(self._alpha)
        srx = np.sin(self._alpha)
        crz = np.cos(angle)
        srz = np.sin(angle)

        d = self._d
        a = self._a
        # self.theda = angle

        transform = np.array(
            [
                [crz, -srz, 0, a],
                [crx * srz, crx * crz, -srx, -d * srx],
                [srx * srz, crz * srx, crx, d * crx],
                [0, 0, 0, 1],
            ],
            dtype=np.float64,
        )

        return transform

@attr.s
class Prismatic(Link):
    min = attr.ib(type=float)
    max = attr.ib(type=float)
