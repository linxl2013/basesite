# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0011_auto_20151117_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='islock',
            field=models.CharField(default=b'0', max_length=1, choices=[(b'0', b'false'), (b'1', b'true')]),
        ),
    ]
