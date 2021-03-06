from tortoise.models import Model
from tortoise import fields
from flask_security import UserMixin, RoleMixin

from sales_bot.default_messages import *


class Telegram_user(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, index=True)
    username = fields.CharField(128, unique=True)
    state = fields.CharField(32, null=True)

    def __str__(self):
        return str(self.telegram_id)


class Shop(Model):
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField('models.Telegram_user', related_name='shops', index=True)
    name = fields.CharField(100)
    description = fields.TextField()
    photo = fields.BinaryField()
    catalog = fields.BooleanField(default=False)


class Products(Model):
    id = fields.IntField(pk=True)
    shop = fields.ForeignKeyField('models.Shop', related_name='products', index=True)
    name = fields.CharField(100, index=True)
    description = fields.TextField()


class Photos(Model):
    id = fields.IntField(pk=True)
    source = fields.BinaryField()
    product = fields.ForeignKeyField('models.Products', related_name='photos', index=True)


class Deals(Model):
    id = fields.IntField(pk=True)
    shop = fields.ForeignKeyField('models.Shop', related_name='deals', index=True)
    customer = fields.ForeignKeyField('models.Telegram_user', related_name='deals', index=True)
    price = fields.IntField()
    state = fields.CharField(32)


class Reviews(Model):
    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField('models.Products', related_name='reviews', index=True)
    customer = fields.ForeignKeyField('models.Telegram_user', related_name='reviews', index=True)
    text = fields.TextField()
    rating = fields.SmallIntField()


class User(Model, UserMixin):
    id = fields.IntField(pk=True)
    email = fields.CharField(254, unique=True)
    password = fields.CharField(255)
    active = fields.BooleanField()
    roles = fields.ManyToManyField(
        'models.Role', related_name='users', through='roles_users'
    )


class Role(Model, RoleMixin):
    id = fields.IntField(pk=True)
    name = fields.CharField(100, unique=True)
    description = fields.CharField(255)
