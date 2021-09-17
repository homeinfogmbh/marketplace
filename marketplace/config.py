"""Configuration file loading."""

from configlib import loadcfg


__all__ = ['CONFIG']


CONFIG = loadcfg('marketplace.conf')
