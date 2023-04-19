# -*- coding: utf-8 -*-

from django.conf.urls import include
from django.views.generic.base import RedirectView
from django.urls import re_path, reverse_lazy


urlpatterns = [
    re_path(
        r'^$',
        RedirectView.as_view(
            url=reverse_lazy('download_gml'), permanent=True
        ),
    ),

    re_path(r'^catastro/', include('catastro.urls')),
]
