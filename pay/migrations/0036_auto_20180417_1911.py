# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-17 19:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0035_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
    ]
