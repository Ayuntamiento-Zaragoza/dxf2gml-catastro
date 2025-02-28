FROM debian:bookworm-slim as builder
MAINTAINER Alberto Gacías <alberto@migasfree.org>

ENV TERM=xterm \
    DEBIAN_FRONTEND=noninteractive \
    USER=root \
    LANG=en_US.utf8 \
    DJANGO_SETTINGS_MODULE=dxf2gml_catastro.settings \
    _BUILD_DEPENDS='python3-dev python3-all debhelper unzip wget python3-pip' \
    _DEPENDS='python3 python3-gdal'

RUN apt-get update && \
    apt-get install -y --no-install-recommends $_BUILD_DEPENDS && \
    apt-get install -y --no-install-recommends $_DEPENDS && \
    wget https://github.com/ayuntamiento-zaragoza/dxf2gml-catastro/archive/master.zip && \
    unzip master.zip && \
    cd dxf2gml-catastro-master && \
    pip install -r requirements/production.txt &&\
    python3 setup.py install && \
    cd .. && \
    rm -rf master.zip && \
    rm -rf dxf2gml-catastro-master && \
    apt-get -y --auto-remove purge $_BUILD_DEPENDS && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY defaults/docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/bin/bash", "/docker-entrypoint.sh"]

EXPOSE 80
