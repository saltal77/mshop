# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-03 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20171222_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='recommended',
            field=models.BooleanField(default=False, verbose_name='Рекоммендуемый'),
        ),
    ]