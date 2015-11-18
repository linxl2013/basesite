# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0009_button_grouppriv_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='islock',
            field=models.CharField(default=datetime.datetime(2015, 11, 17, 15, 0, 58, 871000, tzinfo=utc), max_length=1, choices=[(b'0', b'false'), (b'1', b'true')]),
            preserve_default=False,
        ),
    ]
