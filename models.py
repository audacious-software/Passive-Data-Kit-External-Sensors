# pylint: disable=line-too-long
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from six import python_2_unicode_compatible

from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

@python_2_unicode_compatible
class SensorRegion(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=512)
    identifier = models.SlugField(unique=True, max_length=512, db_index=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.identifier)

    bounds = models.MultiPolygonField(blank=True, null=True)
    center = models.PointField(blank=True, null=True)

    include_sensors = models.BooleanField(default=True)


@python_2_unicode_compatible
class SensorUnit(models.Model):
    name = models.CharField(max_length=512)
    abbreviation = models.CharField(max_length=512)

    description = models.TextField(max_length=4194304, null=True, blank=True)

    base_unit = models.ForeignKey('self', related_name='derivative_units', null=True, blank=True, on_delete=models.SET_NULL)
    base_multiplier = models.FloatField(default=1.0)

    def __str__(self):
        return '%s (%s)' % (self.name, self.abbreviation)


@python_2_unicode_compatible
class SensorMeasurementType(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField(max_length=4194304, null=True, blank=True)

    data_keys = models.TextField(max_length=4194304, null=True, blank=True)

    unit = models.ForeignKey(SensorUnit, on_delete=models.CASCADE)

    minimum_valid_value = models.FloatField(null=True, blank=True)
    maximum_valid_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.unit)


@python_2_unicode_compatible
class SensorModel(models.Model):
    name = models.CharField(max_length=512)
    identifier = models.SlugField(unique=True, max_length=512, db_index=True)

    manufacturer = models.CharField(max_length=512)
    version = models.CharField(max_length=512, null=True, blank=True)

    released = models.DateField(null=True, blank=True)
    retired = models.DateField(null=True, blank=True)

    description = models.TextField(max_length=4194304, null=True, blank=True)

    included_measurements = models.ManyToManyField(SensorMeasurementType, related_name='sensor_models')

    def __str__(self):
        return str(self.name)


@python_2_unicode_compatible
class Sensor(models.Model):
    name = models.CharField(max_length=512)
    identifier = models.SlugField(unique=True, max_length=512, db_index=True)

    description = models.TextField(max_length=4194304, null=True, blank=True)

    model = models.ForeignKey(SensorModel, related_name='sensors', null=True, blank=True, on_delete=models.SET_NULL)

    record_changes_only = models.BooleanField(default=True)

    added = models.DateTimeField(db_index=True)
    last_checked = models.DateTimeField(null=True, blank=True, db_index=True)
    removed = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.identifier)


@python_2_unicode_compatible
class SensorLocation(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='locations', on_delete=models.CASCADE)

    first_observed = models.DateTimeField()
    last_observed = models.DateTimeField()

    location = models.PointField(blank=True, null=True)

    def __str__(self):
        return str(self.location)


@python_2_unicode_compatible
class SensorDataPayload(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='data_payloads', null=True, blank=True, on_delete=models.SET_NULL)

    observed = models.DateTimeField()
    location = models.ForeignKey(SensorLocation, related_name='data_payloads', null=True, blank=True, on_delete=models.SET_NULL)

    definition = JSONField()

    ingested = models.BooleanField(default=False)

    metadata = JSONField(null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.sensor, self.observed)

    def ingest(self):
        pass # Implement later...
