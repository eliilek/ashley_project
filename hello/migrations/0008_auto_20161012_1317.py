# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-12 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0007_auto_20160915_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passing_accuracy_percentage', models.SmallIntegerField(null=True)),
                ('passing_time', models.DurationField(null=True)),
                ('training', models.BooleanField(default=True)),
                ('phase_num', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SessionLength',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('trials', models.SmallIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='responseblock',
            name='training',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='training',
        ),
        migrations.AlterField(
            model_name='responseblock',
            name='phase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hello.Phase'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='phase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hello.Phase'),
        ),
        migrations.AlterField(
            model_name='symbolset',
            name='phase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hello.Phase'),
        ),
        migrations.AddField(
            model_name='sessionlength',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.Subject'),
        ),
    ]
