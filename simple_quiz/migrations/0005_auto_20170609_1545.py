# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 12:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_quiz', '0004_auto_20170609_1437'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
