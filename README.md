Descripción
===========

Servicio web para la conversión de ficheros en formato DXF a [formato GML](http://www.catastro.minhap.gob.es/esp/formatos_intercambio.asp).

Basado en el proyecto [dxf2gmlcatastro](https://github.com/sigdeletras/dxf2gmlcatastro) de Patricio Soriano (SIGdeletras.com) y Marcos Manuel Ortega (Indavelopers).


Requisitos
==========

* Python >= 2.7
* Django >= 1.9
* pygdal (python-gdal) >= 1.10


Especificaciones de los ficheros DXF
====================================

1. En el nombre de la capa se establecerá la referencia catastral (14 dígitos) o la referencia local.
2. Las geometrías deben ser sólidas y estar cerradas (el primer y último punto del polígono deben ser el mismo).


Ejemplos de uso
===============

```bash
$ curl -F "dxf=@file.dxf" -F "code=25831" http://<server>/catastro/json/ > result.json
```

Obtiene un JSON con información de la conversión y el fichero GML resultante.


```bash
$ curl -F "dxf=@file.dxf" -F "code=25831" http://<server>/catastro/gml/ > file.gml
```

Obtiene el fichero en formato GML.
