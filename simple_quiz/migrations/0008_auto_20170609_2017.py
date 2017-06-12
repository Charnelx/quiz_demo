# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_quiz', '0007_auto_20170609_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, default='Misc', help_text='<br /> Try to fit in 128 characters', max_length=128, unique=True, verbose_name='Category name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, help_text='<br />Leave blank for auto-generated slug.', unique=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(blank=True, help_text='<br />Leave blank for auto-generated slug.', unique=True),
        ),
    ]
