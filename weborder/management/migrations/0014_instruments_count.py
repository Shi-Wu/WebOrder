# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0013_homeimg_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='instruments',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
