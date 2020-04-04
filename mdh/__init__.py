try:
    from importlib.metadata import version # type: ignore
except ImportError:
    from importlib_metadata import version # type: ignore

# will this work?
__version__ = version("mdh")
__author__ = "Kevin J. Walchko"
__license__ = "MIT"
