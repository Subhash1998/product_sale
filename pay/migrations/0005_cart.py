# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-10 18:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pay', '0004_auto_20180410_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_pname', models.CharField(max_length=300)),
                ('cart_pprice', models.DecimalField(decimal_places=2, max_digits=20)),
                ('cart_pimage', models.ImageField(blank=True, upload_to='images')),
                ('cart_pdescription', models.CharField(max_length=10000)),
                ('cart_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
