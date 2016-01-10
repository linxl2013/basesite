# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_projectresponsible'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectresponsible',
            old_name='Responsible',
            new_name='responsible',
        ),
    ]
