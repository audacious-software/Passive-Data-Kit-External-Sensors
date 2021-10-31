# pylint: skip-file
# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-30 22:01

from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('identifier', models.SlugField(max_length=512, unique=True)),
                ('description', models.TextField(blank=True, max_length=4194304, null=True)),
                ('record_changes_only', models.BooleanField(default=True)),
                ('added', models.DateTimeField()),
                ('last_checked', models.DateTimeField(blank=True, null=True)),
                ('removed', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorDataPayload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observed', models.DateTimeField()),
                ('definition', django.contrib.postgres.fields.jsonb.JSONField()),
                ('ingested', models.BooleanField(default=False)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_observed', models.DateTimeField()),
                ('last_observed', models.DateTimeField()),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='passive_data_kit_external_sensors.Sensor')),
            ],
        ),
        migrations.CreateModel(
            name='SensorMeasurementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True, max_length=4194304, null=True)),
                ('data_keys', models.TextField(blank=True, max_length=4194304, null=True)),
                ('minimum_valid_value', models.FloatField(blank=True, null=True)),
                ('maximum_valid_value', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('identifier', models.SlugField(max_length=512, unique=True)),
                ('manufacturer', models.CharField(max_length=512)),
                ('version', models.CharField(blank=True, max_length=512, null=True)),
                ('released', models.DateField(blank=True, null=True)),
                ('retired', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=4194304, null=True)),
                ('included_measurements', models.ManyToManyField(related_name='sensor_models', to='passive_data_kit_external_sensors.SensorMeasurementType')),
            ],
        ),
        migrations.CreateModel(
            name='SensorRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('identifier', models.SlugField(max_length=512, unique=True)),
                ('bounds', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('center', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('include_sensors', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('abbreviation', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True, max_length=4194304, null=True)),
                ('base_multiplier', models.FloatField(default=1.0)),
                ('base_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='derivative_units', to='passive_data_kit_external_sensors.SensorUnit')),
            ],
        ),
        migrations.AddField(
            model_name='sensormeasurementtype',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passive_data_kit_external_sensors.SensorUnit'),
        ),
        migrations.AddField(
            model_name='sensordatapayload',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_payloads', to='passive_data_kit_external_sensors.SensorLocation'),
        ),
        migrations.AddField(
            model_name='sensordatapayload',
            name='sensor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_payloads', to='passive_data_kit_external_sensors.Sensor'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensors', to='passive_data_kit_external_sensors.SensorModel'),
        ),
    ]