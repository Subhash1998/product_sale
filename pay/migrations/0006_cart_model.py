# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-10 19:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0005_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='model',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='pay.UserProfile'),
        ),
    ]
