# pylint: disable=line-too-long

from __future__ import print_function

import importlib

from django.conf import settings

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Imports sensor regions from third-party packages.'

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:
            try:
                pdk_api = importlib.import_module(app + '.pdk_api')

                module_sensors = pdk_api.fetch_sensors()

                for sensor in module_sensors:
                    pdk_api.ingest_sensor_data(sensor)
            except ImportError:
                pass
            except AttributeError:
                pass
