# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-09 23:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_quiz', '0009_auto_20170609_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(error_messages={'required': 'You should specify unique name for the quiz'}, help_text='<br />Try to fit in 256 characters', max_length=256, verbose_name='Title'),
        ),
    ]
