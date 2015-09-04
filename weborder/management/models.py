from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField()

    def __unicode__(self):
        return self.user.username


class Instruments(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    author = models.CharField(max_length=128)
    pubDate = models.DateField()
    typ = models.CharField(max_length=128)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Img(models.Model):
    name = models.CharField(max_length=128)
    desc = models.TextField()
    img = models.ImageField(upload_to='image')
    book = models.ForeignKey(Instruments)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class HomeImg(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    img = models.ImageField(upload_to='image')

    def __unicode__(self):
        return self.name

    class META:
        ordering = ['name']


#class Cart(models.Model):
#    userid=models.ForeignKey(MyUser.user)
#    instrid=models.ForeignKey(Instruments.name)
#    count=models.IntegerField()