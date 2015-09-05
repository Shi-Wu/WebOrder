# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_auto_20150904_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeimg',
            name='desc',
            field=models.TextField(default=b'This Is Description Text'),
        ),
    ]
