# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-04 15:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_hotel_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hid', models.IntegerField(default=0)),
                ('text', models.TextField(default='')),
            ],
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='com',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Hotel'),
        ),
    ]
