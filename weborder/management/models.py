# coding :utf-8

from django.db import models
# from django.db import connection
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField()
    login_id = models.IntegerField(default=0)

    @staticmethod
    def get_user(username):
        if username:
            try:
                user = MyUser.objects.get(user__username=username)
            except MyUser.DoesNotExist:
                user = ''
        else:
            user = ''
        return user

    @staticmethod
    def user_logout(username):
        user = MyUser.get_user(username)
        if user:
            return user.user.is_authenticated()
        else:
            return False

    @staticmethod
    def is_already_login(username):
        try:
            user = MyUser.objects.get(user__username=username)
            if user:
                return False
                # return not user.user.is_authenticated()
            else:
                return False
        except MyUser.DoesNotExist:
            return False

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
    count = models.IntegerField(default=1)

    @staticmethod
    def get_type_list():
        book_list = Instruments.objects.all()
        type_list = set()
        for book in book_list:
            type_list.add(book.typ)
        return list(type_list)

    @staticmethod
    def check_item_id(item_id, item_count):
        if item_count > 0 and Instruments.objects.filter(pk=item_id).exists():
            return item_count <= Instruments.objects.get(pk=item_id).count
        return False

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
        return str(self.id)+" "+self.user.nickname + " $" + str(self.sum_price) + \
            " " + str(self.weight)+"Kg "+self.address + " " + self.transport


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

    @staticmethod
    def init_user_cart(user):
        if user == '':
            return False
        else:
            Cart.objects.filter(user=user).delete()

    @staticmethod
    def get_cart_count(usr):
        if usr:
            return Cart.objects.filter(user=usr).count()
        else:
            return 0

    def __unicode__(self):
        return str(self.item_id)+" "+self.user.nickname

    class META:
        ordering = ['item_id']
