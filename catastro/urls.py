# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import download_gml, download_json


urlpatterns = [
    url(r'^gml/$', download_gml, name='download_gml'),
    url(r'^json/$', download_json, name='download_json'),
]
