# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-10 13:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20180210_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='collaborators',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
