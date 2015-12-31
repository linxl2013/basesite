# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='orderby',
            field=models.IntegerField(default=b'0', blank=True),
        ),
    ]
