# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_auto_20150904_1406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='item_id',
            new_name='item',
        ),
    ]
