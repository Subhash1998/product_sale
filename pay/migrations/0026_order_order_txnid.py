# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-14 22:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0025_order_order_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_txnid',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
