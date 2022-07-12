"""Object-relational mappings."""

from __future__ import annotations
from datetime import datetime

from peewee import JOIN
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import ModelSelect

from comcatlib import User
from filedb import File
from mdb import Company, Customer, Tenement
from peeweeplus import JSONModel, MySQLDatabaseProxy, SmallUnsignedIntegerField

from marketplace.config import CONFIG_FILE, get_max_price, get_min_price
from marketplace.exceptions import InvalidPrice, MissingContactInfo


DATABASE = MySQLDatabaseProxy('marketplace', CONFIG_FILE)
USER_FIELDS = {'title', 'description', 'price', 'email', 'phone'}


class MarketplaceModel(JSONModel):
    """Base model for the marketplace."""

    class Meta:
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
    created = DateTimeField(default=datetime.now)

    @classmethod
    def select(cls, *args, cascade: bool = False) -> ModelSelect:
        """Selects offers."""
        if not cascade:
            return super().select(*args)

        return super().select(
            cls, User, Tenement, Customer, Company, *args
        ).join(User).join(Tenement).join(Customer).join(Company).join_from(
            cls, Image, on=Image.offer == cls.id, join_type=JOIN.LEFT_OUTER
        ).group_by(cls.id)

    @classmethod
    def from_json(cls, json: dict, **kwargs) -> Offer:
        """Creates an Offer instance from a JSON-ish dict."""
        if get_min_price() <= (price := json.get('price')) <= get_max_price():
            return super().from_json(json, only=USER_FIELDS, **kwargs)

        raise InvalidPrice(price, get_min_price(), get_max_price())

    def to_json(self, *args, **kwargs) -> dict:
        """Returns a JSON-ish dict."""
        json = super().to_json(*args, **kwargs)
        json['images'] = [image.id for image in self.images]
        return json

    def save(self, *args, **kwargs) -> int:
        """Saves the record."""
        if not self.email and not self.phone:
            raise MissingContactInfo()

        return super().save(*args, **kwargs)


class Image(MarketplaceModel):
    """Image attachment."""

    offer = ForeignKeyField(
        Offer, column_name='offer', backref='images', on_delete='CASCADE'
    )
    file = ForeignKeyField(File, column_name='file')
    index = IntegerField(default=0)

    @classmethod
    def select(cls, *args, cascade: bool = False) -> ModelSelect:
        """Selects offers."""
        if not cascade:
            return super().select(*args)

        return super().select(
            cls, Offer, User, Tenement, Customer, Company, File, *args
        ).join(Offer).join(User).join(Tenement).join(Customer).join(
            Company).join_from(cls, File)
