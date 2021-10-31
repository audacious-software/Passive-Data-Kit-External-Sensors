# pylint: disable=line-too-long

from __future__ import print_function

from builtins import str # pylint: disable=redefined-builtin

import importlib

from django.conf import settings

from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from ...models import SensorRegion

class Command(BaseCommand):
    help = 'Imports sensor regions from third-party packages.'

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:
            try:
                pdk_api = importlib.import_module(app + '.pdk_api')

                module_regions = pdk_api.fetch_sensor_regions()

                for region in module_regions:
                    sensor_region = SensorRegion.objects.filter(identifier=region['identifier']).first()

                    if sensor_region is None:
                        sensor_region = SensorRegion(identifier=region['identifier'], name=region['name'])

                        sensor_region.bounds = GEOSGeometry(region['bounds'])
                        sensor_region.center = sensor_region.bounds.centroid

                        sensor_region.save()

                        print('Imported ' + str(sensor_region) + '.')
            except ImportError:
                pass
            except AttributeError:
                pass
