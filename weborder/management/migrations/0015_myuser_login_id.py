# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0014_instruments_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='login_id',
            field=models.IntegerField(default=0),
        ),
    ]
