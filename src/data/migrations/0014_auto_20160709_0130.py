# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-09 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_auto_20160328_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=19)),
                ('price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('fees', models.DecimalField(decimal_places=4, max_digits=19)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('reporting_name', models.CharField(max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('symbols', models.ManyToManyField(related_name='portfolios', related_query_name='portfolio', through='data.Lot', to='data.Symbol')),
            ],
        ),
        migrations.AddField(
            model_name='lot',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lots', related_query_name='lot', to='data.Portfolio'),
        ),
        migrations.AddField(
            model_name='lot',
            name='symbol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lots', related_query_name='lot', to='data.Symbol'),
        ),
    ]