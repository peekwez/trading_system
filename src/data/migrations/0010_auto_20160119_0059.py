# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 00:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20160109_0614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datavendor',
            old_name='website_url',
            new_name='historical_url',
        ),
        migrations.AddField(
            model_name='datavendor',
            name='quotes_url',
            field=models.URLField(max_length=255, null=True),
        ),
    ]