# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-10 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='size',
            name='sz',
            field=models.CharField(choices=[('S', 'Маленький'), ('M', 'Средний'), ('L', 'Большой')], db_index=True, max_length=1, unique=True, verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Тип'),
        ),
    ]