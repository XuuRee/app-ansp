# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-21 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20171221_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='finished',
            field=models.DateField(blank=True, null=True),
        ),
    ]