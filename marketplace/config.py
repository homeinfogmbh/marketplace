"""Configuration file loading."""

from configlib import loadcfg


__all__ = ['CONFIG', 'MAX_IMAGES', 'MAX_IMAGE_SIZE', 'MAX_PRICE', 'MIN_PRICE']


CONFIG = loadcfg('marketplace.conf')
MAX_IMAGES = CONFIG.getint('limits', 'max_images', fallback=4)
THREE_MB = 3 * 1024 * 1024
MAX_IMAGE_SIZE = CONFIG.getint('limits', 'max_image_size', fallback=THREE_MB)
MAX_PRICE = CONFIG.getint('limits', 'max_price', fallback=9999)
MIN_PRICE = CONFIG.getint('limits', 'min_price', fallback=0)
