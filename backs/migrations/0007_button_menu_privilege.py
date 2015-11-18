# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0006_grouppriv'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privid', models.IntegerField()),
                ('buttonname', models.CharField(max_length=30)),
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
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('module', models.CharField(max_length=30)),
                ('method', models.CharField(max_length=30)),
            ],
        ),
    ]
