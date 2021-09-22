"""Common error handlers."""

from wsgilib import JSONMessage

from marketplace.orm import Offer, Image
from marketplace.exceptions import ImageTooLarge, InvalidPrice, MaxImagesReached


__all__ = ['ERRORS']


ERRORS = {
    Image.DoesNotExist: lambda _: JSONMessage('No such image.', status=404),
    ImageTooLarge: lambda error: JSONMessage(
        'Image too large.', size=error.size, max=error.max_size, status=400),
    InvalidPrice: lambda error: JSONMessage(
        'Invalid price.', value=error.value, min=error.min_price,
        max=error.max_price, status=400),
    MaxImagesReached: lambda error: JSONMessage(
        'Maximum amount of images reached.', max=error.max_images, status=400),
    Offer.DoesNotExist: lambda _: JSONMessage('No such offer.', status=404),
}
