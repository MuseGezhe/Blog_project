# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-04 09:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog_project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_project.Post')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_project.Reader')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
    ]