# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_auto_20150904_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homeimg',
            name='id',
        ),
        migrations.AddField(
            model_name='homeimg',
            name='home_img_id',
            field=models.IntegerField(default=0, serialize=False, auto_created=True, primary_key=True),
            preserve_default=False,
        ),
    ]
