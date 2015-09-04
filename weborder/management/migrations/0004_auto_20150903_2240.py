# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20150903_2054'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Book',
            new_name='Instruments',
        ),
    ]
