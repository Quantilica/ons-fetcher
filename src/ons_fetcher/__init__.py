"""Coletor e conversor Lake Hive de dados abertos do ONS."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ons-fetcher")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["__version__"]
