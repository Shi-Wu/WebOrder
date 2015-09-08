# coding :utf-8

from django.db import models
from django.db import connection
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField()
    # is_login = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username+" "+self.nickname+" "+str(self.permission)


class Instruments(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField(default=0.0)
    author = models.CharField(max_length=128)  # brand
    pubDate = models.DateField()
    typ = models.CharField(max_length=128)  #
    desc = models.TextField(default="")
    weight = models.FloatField(default=0)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Img(models.Model):
    name = models.CharField(max_length=128)
    desc = models.TextField()
    img = models.ImageField(upload_to='image')
    item = models.ForeignKey(Instruments)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class HomeImg(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    img = models.ImageField(upload_to='image')
    desc = models.TextField(default="This Is Description Text")

    def __unicode__(self):
        return self.name

    class META:
        ordering = ['name']


class OrderList(models.Model):
    user = models.ForeignKey(MyUser)
    sum_price = models.FloatField()
    date = models.DateTimeField()
    weight = models.FloatField()
    address = models.CharField(max_length=128)
    transport = models.CharField(max_length=256)

    def __unicode__(self):
        return str(self.id)+" "+self.user.nickname


class OrderDetail(models.Model):
    order_id = models.ForeignKey(OrderList)
    item_id = models.ForeignKey(Instruments)
    count = models.IntegerField()
    price = models.FloatField()  # sold price in all
    weight = models.FloatField()  # all weight

    def __unicode__(self):
        return str(self.order_id)+" "+self.item_id.name

    class META:
        ordering = ['order_id']


class Cart(models.Model):
    user = models.ForeignKey(MyUser)
    item_id = models.ForeignKey(Instruments)
    count = models.IntegerField()
    price = models.FloatField()
    weight = models.FloatField()

    def __unicode__(self):
        return str(self.item_id)+" "+self.user.nickname

    class META:
        ordering = ['item_id']
