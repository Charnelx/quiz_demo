# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 17:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_quiz', '0008_auto_20170609_2017'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='exam',
            new_name='quiz',
        ),
    ]
