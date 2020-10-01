import attr
from collections import namedtuple
from enum import IntFlag
import numpy as np # type: ignore
np.set_printoptions(suppress=True)
from colorama import Fore

JointType =  IntFlag('JointType', 'revolute prismatic revolute_theda revolute_alpha')
mdh_params = namedtuple("mdh_params", "alpha a theta d ")

from math import pi
rad2deg = 180/pi
deg2rad = pi/180

@attr.s(slots=True)
class RevoluteLink:
    """
    RevoluteLink about theta. All other parameters (alpha, a, d) are fixed and
    cannot be changed once the link is created.
    """
    _alpha = attr.ib()
    _a = attr.ib()
    theta = attr.ib()
    _d = attr.ib()
    min = attr.ib(default=-np.pi/2)
    max = attr.ib(default=np.pi/2)

    @max.validator
    def max_check(self, attribute, value):
        if self.min > value:
            raise Exception()

    @property
    def alpha(self):
        return self._alpha

    @property
    def a(self):
        return self._a

    @property
    def d(self):
        return self._d
    #
    # @property
    # def type(self):
    #     return JointType.revolute

    """Some of these params are immutable, how do I do that?"""
    def transform(self, angle):
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

    def __str__(self):
        saa = f"{Fore.CYAN}{self._alpha*rad2deg:4.1f}{Fore.RESET}"
        st = f"{Fore.CYAN}{self.theta*rad2deg:4.1f}{Fore.RESET}"
        sa = f"{Fore.YELLOW}{self._a:4.1f}{Fore.RESET}"
        sd = f"{Fore.YELLOW}{self._d:4.1f}{Fore.RESET}"
        return f"Rev[deg]: alpha: {saa} a: {sa} theta: {st} d: {sd}"
