"""Common exceptions."""

__all__ = ['InvalidPrice']


class InvalidPrice(ValueError):
    """Indicates an invalid price value."""

    def __init__(self, value: int, min_price: int, max_price: int):
        super().__init__(value)
        self.min_price = min_price
        self.max_price = max_price
