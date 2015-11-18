# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backs', '0007_button_menu_privilege'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Button',
        ),
        migrations.DeleteModel(
            name='Grouppriv',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.DeleteModel(
            name='Privilege',
        ),
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(max_length=64),
        ),
    ]
