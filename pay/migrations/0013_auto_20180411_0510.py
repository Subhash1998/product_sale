# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-11 05:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0012_cart_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_user',
            field=models.CharField(max_length=1000),
        ),
    ]
