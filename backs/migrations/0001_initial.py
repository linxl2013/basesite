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
                ('password', models.CharField(max_length=64)),
                ('realname', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=90)),
                ('phone', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=1, choices=[(b'f', b'female'), (b'm', b'male')])),
                ('visits', models.IntegerField()),
                ('lastlogin', models.DateTimeField(null=True, blank=True)),
                ('lastip', models.CharField(max_length=64)),
                ('joined', models.DateTimeField()),
                ('locked', models.DateTimeField(null=True, blank=True)),
                ('islock', models.CharField(default=b'0', max_length=1, choices=[(b'0', b'false'), (b'1', b'true')])),
                ('deleted', models.CharField(default=b'0', max_length=1, choices=[(b'0', b'false'), (b'1', b'true')])),
            ],
        ),
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
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('role', models.CharField(max_length=30)),
                ('desc', models.CharField(max_length=255)),
                ('acl', models.TextField()),
                ('parentid', models.IntegerField()),
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
