# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-19 11:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ['name'], 'verbose_name': 'Цвет', 'verbose_name_plural': 'Цвета'},
        ),
    ]