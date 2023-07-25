"""Configuration file loading."""

from functools import cache, partial

from configlib import load_config


__all__ = [
    "CONFIG_FILE",
    "THREE_MB",
    "get_config",
    "get_max_images",
    "get_max_image_size",
    "get_max_price",
    "get_min_price",
]


CONFIG_FILE = "marketplace.conf"
THREE_MB = 3 * 1024 * 1024

get_config = partial(cache(load_config), CONFIG_FILE)


def get_max_images() -> int:
    """Returns the number of maximally allowed images per offer."""

    return get_config().getint("limits", "max_images", fallback=4)


def get_max_image_size() -> int:
    """Returns the maximally allowed image size for attachments in bytes."""

    return get_config().getint("limits", "max_image_size", fallback=THREE_MB)


def get_max_price() -> int:
    """Returns the maximally allowed price of an offer."""

    return get_config().getint("limits", "max_price", fallback=9999)


def get_min_price() -> int:
    """Returns the minimally allowed price of an offer."""

    return get_config().getint("limits", "min_price", fallback=0)
