# -*- coding: utf-8 -*-

import os


def handle_uploaded_file(f, target):
    path = os.path.dirname(target)
    if not os.path.isdir(path):
        os.makedirs(path)

    with open(target, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
