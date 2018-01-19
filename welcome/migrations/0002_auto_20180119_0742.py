# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-19 07:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameWorld',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'com1x3', max_length=10)),
                ('session', models.CharField(default=b'None', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Kingdom',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=b'None', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name=b'date created')),
                ('off_score', models.IntegerField()),
                ('deff_score', models.IntegerField()),
                ('hero_score', models.IntegerField()),
                ('population', models.IntegerField(default=0)),
                ('kingdom', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='welcome.Kingdom')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('capital', models.IntegerField()),
                ('tribe', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='log',
            name='player',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='welcome.Player'),
        ),
    ]
