# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_auto_20150904_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='book',
            new_name='item_id',
        ),
        migrations.RemoveField(
            model_name='instruments',
            name='id',
        ),
        migrations.RemoveField(
            model_name='orderlist',
            name='id',
        ),
        migrations.AlterField(
            model_name='instruments',
            name='item_id',
            field=models.IntegerField(serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='order_id',
            field=models.CharField(max_length=128, serialize=False, primary_key=True),
        ),
    ]
