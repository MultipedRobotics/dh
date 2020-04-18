import pytest
import mdh
from mdh.models import puma500

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
    with pytest.raises(BobError):
        raise BobError
