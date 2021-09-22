"""Object-relational mappings."""

from __future__ import annotations

from peewee import JOIN, CharField, ForeignKeyField, IntegerField, ModelSelect

from comcatlib import User
from filedb import File
from mdb import Company, Customer, Tenement
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
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects offers."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, User, Tenement, Customer, Company, *args}
        return super().select(*args, **kwargs).join(User).join(Tenement).join(
            Customer).join(Company).join_from(
            cls, Image, on=Image.offer == cls.id, join_type=JOIN.LEFT_OUTER)

    @classmethod
    def from_json(cls, json: dict) -> Offer:
        """Creates an Offer instance from a JSON-ish dict."""
        if (price := json.get('price')) < MIN_PRICE or price > MAX_PRICE:
            raise InvalidPrice(price, MIN_PRICE, MAX_PRICE)

        return super().from_json(json)

    def to_json(self, *args, **kwargs) -> dict:
        """Returns a JSON-ish dict."""
        json = super().to_json(*args, **kwargs)
        json['images'] = [image.id for image in self.images]
        return json

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

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects offers."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Offer, User, Tenement, Customer, Company, File, *args}
        return super().select(*args, **kwargs).join(Offer).join(User).join(
            Tenement).join(Customer).join(Company).join_from(cls, File)
