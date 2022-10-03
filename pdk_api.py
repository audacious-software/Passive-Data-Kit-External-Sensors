# pylint: disable=line-too-long, no-member

from __future__ import print_function

import arrow
import requests

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from django.utils.text import slugify

from passive_data_kit_external_sensors.models import SensorRegion, Sensor, SensorLocation, SensorDataPayload, SensorModel

def fetch_sensors():
    sensors = []

    if hasattr(settings, 'PDK_EXTERNAL_SENSORS_PURPLE_AIR_URL'): # pylint: disable=too-many-nested-blocks
        valid_region = None

        for region in SensorRegion.objects.filter(include_sensors=True):
            if valid_region is None:
                valid_region = region.bounds
            else:
                valid_region = valid_region.union(region.bounds)

        response = requests.get(settings.PDK_EXTERNAL_SENSORS_PURPLE_AIR_URL, timeout=300)

        if response.status_code == 200:
            sensors = response.json()['results']

            region_matches = []

            for sensor in sensors:
                if 'Lat' in sensor and 'Lon' in sensor:
                    sensor_location = GEOSGeometry('POINT(%f %f)' % (sensor['Lon'], sensor['Lat'],))

                    if valid_region.contains(sensor_location):
                        if 'ID' in sensor:
                            sensor['pdk_identifier'] = 'purpleair-' + str(sensor['ID'])

                        if 'LastSeen' in sensor:
                            sensor['pdk_observed'] = arrow.get(sensor['LastSeen']).datetime

                        region_matches.append(sensor)
                # else:
                #    print('INCOMPLETE? ' + json.dumps(sensor, indent=2))

            print('START: ' + str(len(sensors)) + ' - IMPORT: ' + str(len(region_matches)))
        else:
            print('Unexpected HTTP status code for ' + settings.PDK_EXTERNAL_SENSORS_PURPLE_AIR_URL+ ' - ' + str(response.status_code))

    return sensors

def ingest_sensor_data(sensor_data):
    if 'pdk_identifier' in sensor_data:
        identifier = sensor_data['pdk_identifier']

        if identifier.startswith('purpleair-') and ('pdk_observed' in sensor_data) and ('Lat' in sensor_data) and ('Lon' in sensor_data):
            model = None

            if 'Type' in sensor_data:
                model = SensorModel.objects.filter(identifier=slugify(sensor_data['Type'])).first()

                if model is None:
                    model = SensorModel(identifier=slugify(sensor_data['Type']), name=sensor_data['Type'])
                    model.manufacturer = 'Unknown (via Purple Air)'
                    model.save()

            sensor = Sensor.objects.filter(identifier=identifier).first()

            now = timezone.now()

            if sensor is None:
                sensor = Sensor(identifier=identifier)

                if 'Label' in sensor_data:
                    sensor.name = sensor_data['Label'].strip()
                else:
                    sensor.name = identifier

                sensor.added = now
                sensor.model = model

                sensor.save()

            sensor.last_checked = now
            sensor.save()

            payload_when = sensor_data['pdk_observed']

            del sensor_data['pdk_observed']

            sensor_location = GEOSGeometry('POINT(%f %f)' % (sensor_data['Lon'], sensor_data['Lat'],))

            last_location = sensor.locations.all().order_by('-last_observed').first()

            if last_location is None or last_location.location.distance(sensor_location) > 0.00001:
                last_location = SensorLocation.objects.create(sensor=sensor, first_observed=now, last_observed=now, location=sensor_location)
            else:
                if last_location.last_observed != payload_when:
                    last_location.last_observed = payload_when
                    last_location.save()

            last_payload = sensor.data_payloads.filter(observed__gte=payload_when).first()

            if last_payload is None:
                print('ADDING PAYLOAD...')
                data_payload = SensorDataPayload(sensor=sensor, observed=payload_when, location=last_location)
                data_payload.definition = sensor_data
                data_payload.save()
