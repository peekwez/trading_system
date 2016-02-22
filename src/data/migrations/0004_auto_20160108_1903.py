# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-08 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20160108_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exchange',
            name='timezone_offset',
        ),
        migrations.AddField(
            model_name='exchange',
            name='utc_offset',
            field=models.CharField(default='UTC', max_length=6),
        ),
    ]