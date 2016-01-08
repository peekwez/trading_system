# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-08 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('price_date', models.DateTimeField()),
                ('open_price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('high_price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('low_price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('close_price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('adj_close_price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('volume', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataVendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('website_url', models.URLField(max_length=255, null=True)),
                ('support_email', models.EmailField(max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('abbrev', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=255, null=True)),
                ('currency', models.CharField(max_length=64)),
                ('timezone_offset', models.TimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('ticker', models.CharField(max_length=255)),
                ('instrument', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=255, null=True)),
                ('sector', models.CharField(max_length=255, null=True)),
                ('currency', models.CharField(max_length=32, null=True)),
                ('exchange', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='symbols', related_query_name='symbol', to='data.Exchange')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='dailyprice',
            name='date_vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='daily_prices', related_query_name='daily_price', to='data.DataVendor'),
        ),
        migrations.AddField(
            model_name='dailyprice',
            name='symbol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='daily_prices', related_query_name='daily_price', to='data.Symbol'),
        ),
    ]
