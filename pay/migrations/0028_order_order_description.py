# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-14 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0027_auto_20180414_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_description',
            field=models.CharField(blank=True, max_length=10000),
        ),
    ]
