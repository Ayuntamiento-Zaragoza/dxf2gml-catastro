# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy


urlpatterns = [
    url(
        r'^$',
        RedirectView.as_view(
            url=reverse_lazy('download_gml'), permanent=True
        ),
    ),

    url(r'^catastro/', include('catastro.urls')),
]
