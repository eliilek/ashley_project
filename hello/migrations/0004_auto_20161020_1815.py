# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-20 23:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_subject_training'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='singleset',
            options={'verbose_name': 'Single Set'},
        ),
        migrations.AlterModelOptions(
            name='symbolset',
            options={'verbose_name': 'Symbol Set'},
        ),
        migrations.AlterField(
            model_name='response',
            name='modifier',
            field=models.BooleanField(verbose_name=b'!!!!!'),
        ),
        migrations.AlterField(
            model_name='singleset',
            name='correct_response',
            field=models.CharField(max_length=1, verbose_name=b'Option Number of Correct Response (1, 2, or 3)'),
        ),
        migrations.AlterField(
            model_name='singleset',
            name='modifier',
            field=models.BooleanField(verbose_name=b'!!!!!'),
        ),
        migrations.AlterField(
            model_name='symbol',
            name='image',
            field=models.ImageField(upload_to=b'symbols'),
        ),
    ]