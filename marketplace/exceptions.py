"""Common exceptions."""


__all__ = ['ImageTooLarge', 'InvalidPrice', 'MaxImagesReached']


class ImageTooLarge(Exception):
    """Indicates that an image is too large."""

    def __init__(self, size: int, max_size: int):
        super().__init__()
        self.size = size
        self.max_size = max_size


class InvalidPrice(ValueError):
    """Indicates an invalid price value."""

    def __init__(self, value: int, min_price: int, max_price: int):
        super().__init__(value)
        self.min_price = min_price
        self.max_price = max_price


class MaxImagesReached(Exception):
    """Indicates that the maximum amount of images has been reached."""

    def __init__(self, max_images: int):
        super().__init__()
        self.max_images = max_images
