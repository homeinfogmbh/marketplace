"""Common functions."""

from peewee import ModelSelect

from comcatlib import User
from filedb import File

from marketplace.config import MAX_IMAGES, MAX_IMAGE_SIZE
from marketplace.exceptions import ImageTooLarge, MaxImagesReached
from marketplace.orm import Offer, Image


__all__ = [
    'get_offers',
    'get_offer',
    'add_offer',
    'get_images',
    'get_image',
    'add_image'
]


def get_offers(user: User) -> ModelSelect:
    """Yields the user's offers."""

    return Offer.select().where(Offer.user == user)


def get_offer(ident: int, user: User) -> Offer:
    """Returns the given offer."""

    return get_offers(user).where(Offer.id == ident).get()


def add_offer(json: dict, user: User) -> Offer:
    """Adds a new offer."""

    offer = Offer.from_json(json)
    offer.user = user
    offer.save()
    return offer


def get_images(offer: Offer) -> ModelSelect:
    """Yields the offer's images."""

    return offer.images


def get_image(ident: int, offer: Offer) -> Image:
    """Returns the given image."""

    return get_images(offer).where(Image.id == ident).get()


def add_image(offer: Offer, image: bytes, *, index: int = 0) -> Image:
    """Adds an image attachment to an offer."""

    if offer.images.count() > MAX_IMAGES:
        raise MaxImagesReached(MAX_IMAGES)

    if (image_size := len(image)) > MAX_IMAGE_SIZE:
        raise ImageTooLarge(image_size, MAX_IMAGE_SIZE)

    image = Image(offer=offer, file=File.from_bytes(image), index=index)
    image.save()
    return image
