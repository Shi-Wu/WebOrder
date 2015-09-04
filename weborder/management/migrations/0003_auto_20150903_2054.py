# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_homepic'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HomePic',
            new_name='HomeImg',
        ),
    ]
