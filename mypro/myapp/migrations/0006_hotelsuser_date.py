# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 13:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20160502_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelsuser',
            name='date',
            field=models.DateField(auto_now=True, default=datetime.datetime(2016, 5, 3, 13, 41, 24, 959841, tzinfo=utc)),
            preserve_default=False,
        ),
    ]