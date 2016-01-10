# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20151228_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectResponsible',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projectid', models.IntegerField()),
                ('Responsible', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
