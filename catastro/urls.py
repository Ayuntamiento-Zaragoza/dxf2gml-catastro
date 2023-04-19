# -*- coding: utf-8 -*-

from django.urls import re_path

from .views import download_gml, download_json


urlpatterns = [
    re_path(r'^gml/$', download_gml, name='download_gml'),
    re_path(r'^json/$', download_json, name='download_json'),
]
