# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0002_auto_20151022_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('role', models.CharField(max_length=30)),
                ('desc', models.CharField(max_length=255)),
                ('acl', models.TextField()),
            ],
        ),
    ]
