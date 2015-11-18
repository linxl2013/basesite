# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0010_account_islock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='deleted',
            field=models.CharField(default=b'0', max_length=1, choices=[(b'0', b'false'), (b'1', b'true')]),
        ),
    ]
