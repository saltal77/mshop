# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-11 12:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20171211_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Позиция заказа', 'verbose_name_plural': 'Позиции заказа'},
        ),
    ]
