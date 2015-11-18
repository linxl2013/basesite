# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0008_auto_20151113_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parentid', models.IntegerField()),
                ('buttontitle', models.CharField(max_length=30)),
                ('buttonno', models.CharField(max_length=30)),
                ('onclick', models.CharField(max_length=30)),
                ('group', models.CharField(max_length=30)),
                ('module', models.CharField(max_length=30)),
                ('method', models.CharField(max_length=30)),
                ('orderby', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Grouppriv',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupid', models.IntegerField()),
                ('buttonid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parentid', models.IntegerField()),
                ('menuname', models.CharField(max_length=30)),
                ('menuurl', models.CharField(max_length=255)),
                ('menuorder', models.IntegerField()),
            ],
        ),
    ]
