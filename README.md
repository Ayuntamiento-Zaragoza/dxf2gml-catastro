Descripción
===========

Servicio web para la conversión de ficheros en formato DXF a [formato GML](https://www.catastro.hacienda.gob.es/documentos/formatos_intercambio/Formato%20GML%20parcela%20catastral.pdf).

Basado en el proyecto [dxf2gmlcatastro](https://github.com/sigdeletras/dxf2gmlcatastro) de Patricio Soriano (SIGdeletras.com) y Marcos Manuel Ortega (Indavelopers).

Basado también en el proyecto [ParCatGML](https://github.com/psigcat/ParCatGML) para actualizar el formato GML a la versión 4.0.


Requisitos
==========

* Python >= 3.6
* Django >= 4.2
* pygdal (python-gdal) >= 3.6.2


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

Obtiene el fichero en formato GML 4.0.
