try:
    # 3.8
    from importlib.metadata import version # type: ignore
except ImportError:
    # <= 3.7
    from importlib_metadata import version # type: ignore

# will this work?
__version__ = version("mdh")
__author__ = "Kevin J. Walchko"
__license__ = "MIT"

from .kinematic_chain import UnReachable
