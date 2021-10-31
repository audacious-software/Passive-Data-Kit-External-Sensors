# pylint: disable=line-too-long
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis import admin
from django.utils.html import format_html

from .models import SensorRegion, SensorUnit, SensorMeasurementType, SensorModel, Sensor, SensorLocation, SensorDataPayload

# def reset_visualizations(modeladmin, request, queryset): # pylint: disable=unused-argument
#     for visualization in queryset:
#         visualization.last_updated = datetime.datetime.min
#
#         visualization.save()
#
# reset_visualizations.description = 'Reset visualizations'

@admin.register(SensorRegion)
class SensorRegionAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'identifier', 'center', 'include_sensors')
    list_filter = ('include_sensors',)
    search_fields = ['name', 'identifier']

    # actions = [reset_visualizations]


@admin.register(SensorUnit)
class SensorUnitAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'abbreviation', 'base_unit', 'base_multiplier')
    list_filter = ('base_unit',)
    search_fields = ['name', 'abbreviation', 'description']


@admin.register(SensorMeasurementType)
class SensorMeasurementTypeAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'unit', 'minimum_valid_value', 'maximum_valid_value',)
    list_filter = ('unit',)
    search_fields = ['name', 'description', 'data_keys']


@admin.register(SensorModel)
class SensorModelAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'identifier', 'manufacturer', 'version', 'released', 'retired')
    list_filter = ('released', 'retired', 'manufacturer',)
    search_fields = ['name', 'identifier', 'manufacturer', 'description']


@admin.register(Sensor)
class SensorAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'model', 'last_checked', 'added', 'removed',)
    list_filter = ('added', 'last_checked', 'removed', 'record_changes_only', 'model')
    search_fields = ['name', 'identifier', 'description']


@admin.register(SensorLocation)
class SensorLocationAdmin(admin.OSMGeoAdmin):
    list_display = ('sensor', 'first_observed', 'last_observed', 'location')
    list_filter = ('first_observed', 'last_observed',)
    search_fields = ['sensor__name']
    readonly_fields = ('sensor_link',)
    exclude = ('sensor',)

    readonly_fields = ('sensor_link',)

    def sensor_link(self, instance): # pylint: disable=no-self-use
        return format_html(
            '<a href="../../../sensor/{0}/change/">{1}</a>',
            instance.sensor.pk,
            str(instance.sensor),
        )

    sensor_link.short_description = "Sensor"


@admin.register(SensorDataPayload)
class SensorDataPayloadAdmin(admin.OSMGeoAdmin):
    list_display = ('sensor', 'observed', 'ingested', 'location')
    list_filter = ('observed', 'ingested',)
    search_fields = ['definition', 'metadata', 'sensor__name']
    exclude = ('sensor', 'location',)

    readonly_fields = ('sensor_location',)

    def sensor_location(self, instance): # pylint: disable=no-self-use
        return format_html(
            '<a href="../../../sensor/{0}/change/">{1}</a>: <a href="../../../sensorlocation/{2}/change/">{3}</a>',
            instance.sensor.pk,
            str(instance.sensor),
            instance.location.pk,
            str(instance.location),
        )

    sensor_location.short_description = "Sensor & Location"
