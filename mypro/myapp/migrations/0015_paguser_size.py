# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-05 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_paguser_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='paguser',
            name='size',
            field=models.CharField(default='', max_length=200),
        ),
    ]
