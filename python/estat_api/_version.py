"""_version.py
version information
"""

from importlib import metadata

try:
    if __package__:
        __version__ = metadata.version(__package__)
    else:
        __version__ = 'unknown'
except metadata.PackageNotFoundError:
    __version__ = 'unknown'

__all__ = ['__version__']
