# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_auto_20150904_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.IntegerField(serialize=False, auto_created=True, primary_key=True),
        ),
    ]
