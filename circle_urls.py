"""Passive Data Kit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import django

from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', django.contrib.admin.site.urls),
    url(r'^data/sensors', include('passive_data_kit_external_sensors.urls')),
    url(r'^data/', include('passive_data_kit.urls')),
]