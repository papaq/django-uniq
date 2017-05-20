# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-20 14:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'faculties',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GroupStack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('info', models.TextField(blank=True, null=True)),
                ('year_enter', models.DateTimeField()),
                ('year_graduate', models.DateTimeField()),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupstacks', to='channels.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'universities',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='group_stack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='channels.GroupStack'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculties', to='channels.University'),
        ),
    ]
