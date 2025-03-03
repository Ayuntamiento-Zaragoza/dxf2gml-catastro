FROM debian:bookworm-slim AS builder
LABEL maintainer="Alberto Gacías <alberto@migasfree.org>"

ARG VERSION=master

ENV VERSION=${VERSION}

RUN echo ${VERSION} > /VERSION

ENV TERM=xterm \
    DEBIAN_FRONTEND=noninteractive \
    USER=root \
    LANG=en_US.utf8 \
    DJANGO_SETTINGS_MODULE=dxf2gml_catastro.settings \
    _BUILD_DEPENDS='git python3-dev python3-all debhelper unzip wget libgdal-dev g++' \
    _DEPENDS='python3 python3-venv python3-minimal python3-pip python3-gdal'

RUN apt-get update && \
    apt dist-upgrade -y && \
    apt install -y --no-install-recommends apt-utils && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    echo "es_ES.UTF-8 UTF-8" >> /etc/locale.gen && \
    apt install -y --no-install-recommends locales && \
    dpkg-reconfigure locales && \
    update-locale LANG=$LANG && \
    apt-get install -y --no-install-recommends $_BUILD_DEPENDS && \
    apt-get install -y --no-install-recommends $_DEPENDS && \
    python3 -m venv /venv && \
    . /venv/bin/activate  && \
    pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir --upgrade pip
    # python3 -m pip install --no-cache-dir --upgrade setuptools wheel

RUN cd / && \
    . /venv/bin/activate && \
    git clone https://github.com/ayuntamiento-zaragoza/dxf2gml-catastro && \
    cd /dxf2gml-catastro && \
    git checkout $(cat /VERSION)

RUN  cd / && \
    . /venv/bin/activate && \
    cd /dxf2gml-catastro && \
    pip install --no-cache-dir -r requirements/production.txt && \
    python3 setup.py install && \
    rm -rf /dxf2gml-catastro

RUN apt-get -y --auto-remove purge $_BUILD_DEPENDS && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY defaults/docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/bin/bash", "/docker-entrypoint.sh"]

EXPOSE 80
