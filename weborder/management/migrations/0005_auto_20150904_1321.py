# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_auto_20150903_2240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('price', models.FloatField()),
                ('weight', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('price', models.FloatField()),
                ('weight', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_id', models.CharField(max_length=128)),
                ('sum_price', models.FloatField()),
                ('date', models.DateTimeField()),
                ('weight', models.FloatField()),
                ('address', models.CharField(max_length=128)),
                ('transport', models.CharField(max_length=256)),
                ('user', models.ForeignKey(to='management.MyUser')),
            ],
        ),
        migrations.AddField(
            model_name='instruments',
            name='desc',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='instruments',
            name='item_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='instruments',
            name='weight',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='item_id',
            field=models.ForeignKey(to='management.Instruments'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order_id',
            field=models.ForeignKey(to='management.OrderList'),
        ),
        migrations.AddField(
            model_name='cart',
            name='item_id',
            field=models.ForeignKey(to='management.Instruments'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(to='management.MyUser'),
        ),
    ]
