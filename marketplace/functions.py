"""Common functions."""

from typing import Optional

from peewee import ModelSelect

from comcatlib import User
from filedb import File
from mdb import Customer, Tenement

from marketplace.config import MAX_IMAGES, MAX_IMAGE_SIZE
from marketplace.exceptions import ImageTooLarge, MaxImagesReached
from marketplace.orm import Offer, Image


__all__ = [
    'get_offers',
    'get_offer',
    'add_offer',
    'get_image',
    'add_image'
]


def get_offers(*, user: Optional[User] = None,
               customer: Optional[Customer] = None) -> ModelSelect:
    """Yields the user's offers."""

    if user is None and customer is None:
        raise TypeError('Must specify either user or customer.')

    condition = True

    if user is not None:
        condition &= Offer.user == user

    if customer is not None:
        condition &= Tenement.customer == customer

    return Offer.select(cascade=True).where(condition)


def get_offer(ident: int, *, user: Optional[User] = None,
              customer: Optional[Customer] = None) -> Offer:
    """Returns the given offer."""

    return get_offers(user=user, customer=customer).where(
        Offer.id == ident).get()


def add_offer(json: dict, user: User) -> Offer:
    """Adds a new offer."""

    offer = Offer.from_json(json)
    offer.user = user
    offer.save()
    return offer


def get_image(ident: int, offer: Offer) -> Image:
    """Returns the given image."""

    return Image.select(cascade=True).where(
        (Image.id == ident) & (Image.offer == offer)
    ).get()


def add_image(offer: Offer, image: bytes, *, index: int = 0) -> Image:
    """Adds an image attachment to an offer."""

    if offer.images.count() > MAX_IMAGES:
        raise MaxImagesReached(MAX_IMAGES)

    if (image_size := len(image)) > MAX_IMAGE_SIZE:
        raise ImageTooLarge(image_size, MAX_IMAGE_SIZE)

    image = Image(offer=offer, file=File.from_bytes(image), index=index)
    image.save()
    return image
