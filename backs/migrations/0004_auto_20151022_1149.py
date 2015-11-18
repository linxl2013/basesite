# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0003_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='id',
            field=models.IntegerField(max_length=8, serialize=False, primary_key=True),
        ),
    ]
