import pytest
import mdh
import sys
from mdh.link import mdh_params, JointType
from mdh.kinematic_chain import KinematicChain
# from mdh.robots import puma560

# def test_dummy():
#     assert True

# @pytest.mark.xfail
# def test_dummy_2():
#     assert False

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_exception():
    with pytest.raises(Exception):
        raise Exception

class BobError(Exception):
    pass

def test_exception_2():
    print(mdh.__version__)
    for s in sys.path:
        print(s)
    with pytest.raises(BobError):
        raise BobError
