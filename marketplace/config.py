"""Configuration file loading."""

from configlib import loadcfg


__all__ = ['CONFIG', 'MAX_IMAGES', 'MAX_PRICE', 'MIN_PRICE']


CONFIG = loadcfg('marketplace.conf')
MAX_IMAGES = CONFIG.getint('limits', 'max_images', fallback=4)
MAX_PRICE = CONFIG.getint('limits', 'max_price', fallback=9999)
MIN_PRICE = CONFIG.getint('limits', 'max_price', fallback=0)
