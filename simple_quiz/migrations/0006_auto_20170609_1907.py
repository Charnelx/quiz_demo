# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_quiz', '0005_auto_20170609_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='<br />Leave blank for auto-generated slug.', unique=True),
        ),
    ]
