"""Loads typing module from appropriate package

    TypedDict, Protocol were added in python3.8, typing_extensions is a backport that makes these available for
    python35+. See https://pypi.org/project/typing-extensions/
"""

try:
    from typing import Protocol, TypedDict
except ImportError:
    from typing_extensions import Protocol, TypedDict
