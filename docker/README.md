Build container
===============

```sh
docker build --build-arg VERSION=$(cat ../VERSION) -t dxf2gml-catastro .
```

Run container
=============

```sh
docker run --name=dxf2gml-catastro -p 80:80 -d dxf2gml-catastro
```
