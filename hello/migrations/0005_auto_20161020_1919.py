# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-21 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_auto_20161020_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='image',
            field=models.ImageField(upload_to=b'static/hello'),
        ),
    ]
