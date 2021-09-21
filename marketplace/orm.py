"""Object-relational mappings."""

from __future__ import annotations

from peewee import CharField, ForeignKeyField, IntegerField

from comcatlib import User
from filedb import File
from peeweeplus import JSONModel, MySQLDatabase, SmallUnsignedIntegerField

from marketplace.config import CONFIG, MAX_PRICE, MIN_PRICE
from marketplace.exceptions import InvalidPrice


DATABASE = MySQLDatabase.from_config(CONFIG)


class MarketplaceModel(JSONModel):
    """Base model for the marketplace."""

    class Meta:     # pylint: disable=C0115,R0903
        database = DATABASE
        schema = database.database


class Offer(MarketplaceModel):
    """An offer."""

    user = ForeignKeyField(User, column_name='user')
    title = CharField(30)
    description = CharField(640)
    price = SmallUnsignedIntegerField()     # in EUR
    email = CharField(32, null=True)
    phone = CharField(32, null=True)

    @classmethod
    def from_json(cls, json: dict) -> Offer:
        """Creates an Offer instance from a JSON-ish dict."""
        if (price := json.get('price')) < MIN_PRICE or price > MAX_PRICE:
            raise InvalidPrice(price, MIN_PRICE, MAX_PRICE)

        return super().from_json(json)

    def save(self, *args, **kwargs) -> int:
        """Saves the record."""
        if not self.email or not self.phone:
            raise ValueError('Must either specify email or phone number.')

        return super().save(*args, **kwargs)


class Image(MarketplaceModel):
    """Image attachment."""

    offer = ForeignKeyField(
        Offer, column_name='offer', backref='images', on_delete='CASCADE')
    file = ForeignKeyField(File, column_name='file')
    index = IntegerField(default=0)
