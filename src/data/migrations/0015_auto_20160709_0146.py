# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-09 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_auto_20160709_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='fees',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]
