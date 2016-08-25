# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-14 18:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_time', models.DurationField()),
                ('stimulus_type', models.BooleanField(choices=[(True, b'!!!!!'), (False, b'?????')])),
                ('stimulus', models.SmallIntegerField()),
                ('responses', models.CharField(max_length=5)),
                ('correct_response', models.SmallIntegerField()),
                ('given_response', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ResponseBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase', models.SmallIntegerField(choices=[(1, b'Phase 1 - Training'), (2, b'Phase 1 - Testing'), (3, b'Phase 2 - Training'), (4, b'Phase 2 - Testing'), (5, b'Phase 3 - Training'), (6, b'Phase 3 - Testing'), (7, b'Phase 4 - Training'), (8, b'Phase 4 - Testing'), (9, b'Phase 5 - Training'), (10, b'Phase 5 - Testing')])),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('phase', models.SmallIntegerField(choices=[(1, b'Phase 1 - Training'), (2, b'Phase 1 - Testing'), (3, b'Phase 2 - Training'), (4, b'Phase 2 - Testing'), (5, b'Phase 3 - Training'), (6, b'Phase 3 - Testing'), (7, b'Phase 4 - Training'), (8, b'Phase 4 - Testing'), (9, b'Phase 5 - Training'), (10, b'Phase 5 - Testing')])),
            ],
        ),
        migrations.CreateModel(
            name='SymbolSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Greeting',
        ),
        migrations.AddField(
            model_name='responseblock',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hello.Subject'),
        ),
        migrations.AddField(
            model_name='responseblock',
            name='symbol_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.SymbolSet'),
        ),
        migrations.AddField(
            model_name='response',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.Subject'),
        ),
    ]