# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-22 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0002_auto_20180119_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='kingdom',
            name='kid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kingdom',
            name='world',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='welcome.GameWorld'),
        ),
        migrations.AddField(
            model_name='log',
            name='world',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='welcome.GameWorld'),
        ),
        migrations.AddField(
            model_name='player',
            name='pid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='world',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='welcome.GameWorld'),
        ),
        migrations.AlterField(
            model_name='gameworld',
            name='name',
            field=models.CharField(default='com1x3', max_length=10),
        ),
        migrations.AlterField(
            model_name='gameworld',
            name='session',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='kingdom',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='kingdom',
            name='name',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='log',
            name='timestamp',
            field=models.DateTimeField(verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='player',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]