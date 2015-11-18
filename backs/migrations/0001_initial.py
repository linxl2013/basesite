# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=10)),
                ('account', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=32)),
                ('realname', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=90)),
                ('phone', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=1, choices=[(b'f', b'female'), (b'm', b'male')])),
                ('visits', models.IntegerField()),
                ('join', models.DateTimeField()),
                ('locked', models.DateTimeField()),
                ('deleted', models.CharField(max_length=1, choices=[(b'0', b'false'), (b'1', b'true')])),
            ],
        ),
    ]
