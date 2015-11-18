# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0005_auto_20151022_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grouppriv',
            fields=[
                ('group', models.IntegerField(serialize=False, primary_key=True)),
                ('module', models.CharField(max_length=30)),
                ('method', models.CharField(max_length=30)),
            ],
        ),
    ]
