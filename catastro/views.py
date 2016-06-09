# -*- coding: utf-8 -*-

import os
import json

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .utils import handle_uploaded_file

import dxf2gml


def get_gml(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid parameters')

    dxf = request.FILES.get('dxf')
    code = request.POST.get('code', dxf2gml.EPSG_DEFAULT)

    if not dxf:
        return HttpResponseBadRequest('Invalid parameters')

    filename, _ = os.path.splitext(dxf.name)
    target = os.path.join(settings.MEDIA_ROOT, dxf.name)
    handle_uploaded_file(dxf, target)

    ret, output = dxf2gml.dxf2gml(target, code)
    os.remove(target)

    if not ret:
        return HttpResponseBadRequest(output)

    return output


@csrf_exempt
def download_gml(request):
    output = get_gml(request)
    if isinstance(output, HttpResponse):
        return output

    response = HttpResponse(output['gml'], content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s.gml' % filename

    return response


@csrf_exempt
def download_json(request):
    output = get_gml(request)
    if isinstance(output, HttpResponse):
        return output

    return JsonResponse(output, safe=False)
