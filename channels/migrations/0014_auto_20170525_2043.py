# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-25 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0013_university_short_titles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='short_titles',
            field=models.CharField(default='', help_text='Input short names, dividing by coma', max_length=100),
        ),
    ]