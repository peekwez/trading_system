# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-28 20:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_auto_20160121_0115'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='symbol',
            unique_together=set([('ticker',)]),
        ),
    ]
