# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-14 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20171213_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='enable_comments',
            field=models.BooleanField(default=True, verbose_name='Разрешить комментарий'),
        ),
    ]
