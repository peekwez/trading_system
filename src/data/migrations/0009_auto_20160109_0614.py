# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-09 06:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20160109_0532'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dailyprice',
            options={'ordering': ('-price_date', 'symbol')},
        ),
    ]