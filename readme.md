# Modified Denavit–Hartenberg (mdh)

[![Actions Status](https://github.com/MultipedRobotics/dh/workflows/CheckPackage/badge.svg)](https://github.com/MultipedRobotics/dh/actions)
![GitHub](https://img.shields.io/github/license/multipedrobotics/dh)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mdh)
![PyPI](https://img.shields.io/pypi/v/mdh)


<img src="https://upload.wikimedia.org/wikipedia/commons/d/d8/DHParameter.png" width="600px">

[Modified Denavit-Hartenberg parameters](https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters#Modified_DH_parameters)

Build kinematic chains using the modified Denavit-Hartenberg paramters

- d: offset along previous z to the common normal
- theta: angle about previous z, from old x to new x
- a: length of the common normal, assuming a revolute joint, this is the radius about previous z.
- alpha: angle about common normal, from old z axis to new z axis

## Inspiration

You should probably use one of these, they inspired me to write a simpler
module for my needs:

- [pybotics](https://github.com/nnadeau/pybotics)
- [pytransform3d](https://github.com/rock-learning/pytransform3d)
- [robopy](https://github.com/MultipedRobotics/robopy)
- [tinyik](https://github.com/lanius/tinyik), uses `open3d` to visualize the mechanism

## Example

```python
import numpy as np
from mdh.kinematic_chain import KinematicChain

# make it print better
np.set_printoptions(suppress=True)

# modified DH parameters: alpha a theta d
# types: revolute=1, prismatic=2 (not implemented yet)
dh = [
    {'alpha': 0,  'a': 0, 'theta': 0, 'd': 0, 'type': 1},
    {'alpha': pi/2, 'a': 52, 'theta': 0, 'd': 0, 'type': 1},
    {'alpha': 0, 'a': 89, 'theta': 0, 'd': 0, 'type': 1},
    {'alpha': 0, 'a': 90, 'theta': 0, 'd': 0, 'type': 1},
    {'alpha': 0, 'a': 95, 'theta': 0, 'd': 0, 'type': 1}
]

kc = KinematicChain.from_parameters(dh)

# forward kinematics
angles = np.deg2rad([-45.00, 77.41, -98.15, -69.27, 0])
t = kc.forward(angles)
print(f">> {t}")

# inverse kinematics
pt = [110,0,-70]
deg = kc.inverse(pt)
rad = np.rad2deg(deg)
print(f">> {rad}")
```

# MIT License

**Copyright (c) 2019 Kevin J. Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
