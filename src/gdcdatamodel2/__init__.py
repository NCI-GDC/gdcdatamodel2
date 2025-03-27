import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import distribution
else:
    from importlib_metadata import distribution

__distribution = distribution(__name__)
VERSION = __distribution.version

__all__ = ["VERSION"]
