# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-05 03:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0041_auto_20180424_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='media/images'),
        ),
    ]
