# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-10 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0007_remove_cart_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='username',
            field=models.CharField(default=True, max_length=1000),
        ),
    ]
