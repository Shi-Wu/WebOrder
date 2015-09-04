# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_auto_20150904_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instruments',
            name='desc',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='instruments',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
