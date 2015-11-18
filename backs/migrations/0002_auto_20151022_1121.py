# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='join',
            new_name='joined',
        ),
    ]
