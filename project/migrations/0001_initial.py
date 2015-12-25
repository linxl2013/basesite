# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projectname', models.CharField(max_length=255)),
                ('projectcode', models.CharField(max_length=255)),
                ('starttime', models.DateTimeField(null=True, blank=True)),
                ('endtime', models.DateTimeField(null=True, blank=True)),
                ('desc', models.TextField(null=True, blank=True)),
                ('createuserid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Projectmodule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('parentid', models.IntegerField()),
                ('desc', models.TextField(null=True, blank=True)),
                ('createuserid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('desc', models.TextField(null=True, blank=True)),
                ('projectid', models.IntegerField()),
                ('createuserid', models.IntegerField()),
                ('attnid', models.IntegerField()),
                ('starttime', models.DateTimeField(null=True, blank=True)),
                ('estimatetime', models.DateTimeField(null=True, blank=True)),
                ('endtime', models.DateTimeField(null=True, blank=True)),
                ('version', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=10)),
                ('priority', models.CharField(default=b'general', max_length=10, choices=[(b'urgent', b'urgent'), (b'priority', b'priority'), (b'general', b'general'), (b'behind', b'behind')])),
            ],
        ),
    ]
