#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016-2025 Jose Antonio Chavarría <jachavar@gmail.com>
# Copyright (c) 2016-2023 Alberto Gacías <alberto@migasfree.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import json
import glob

__author__ = [
    'Jose Antonio Chavarría <jachavar@gmail.com>',
    'Alberto Gacías <alberto@migasfree.org>',
]
__license__ = 'GPLv3'

"""
Descripción
===========

El script genera un fichero GML de parcela catastral según las especificaciones de Catastro.

Basado en https://github.com/sigdeletras/dxf2gmlcatastro (Patricio Soriano :: SIGdeletras.com)


Especificaciones
================
    * http://www.catastro.minhap.gob.es/esp/formatos_intercambio.asp

    * Cada parcela debe estar en una capa en cuyo nombre se establecerá su referencia.

    * No se permiten incorporar en el mismo fichero dxf parcelas con referencias catastrales y referencias locales mezcladas, todas deben ser del mismo tipo, o bien locales o bien catastrales.

    * Se asume referencia catastral si la longitud de la referencia es de 14 caracteres.

    * Las geometrías deben ser sólidas y estar cerradas (el primer y último punto del polígono deben ser el mismo)


Requisitos
==========

Es necesario tener instalado Python y el módulo GDAL (python3-gdal).


Ejemplos de uso
===============

    * python3 dxf2gml.py <parcela1.dxf>
         generará el fichero parcela1.gml

    * python3 dx2fgml.py <parcela1.dxf> 25831
         generará el fichero parcela1.gml usando el código EPSG 25831

    * python3 dxf2gml.py <mi_directorio>
         generará un fichero .gml por cada fichero .dxf que se encuentre en mi_directorio
"""

try:
    from osgeo import ogr
except ImportError:
    print('Error: python3-gdal no instalado')
    sys.exit(1)

# Sistemas de referencia de coordenadas
EPSG_ZONES = [
    '25828',  # ETRS89 / UTM zone 28N
    '25829',  # ETRS89 / UTM zone 29N
    '25830',  # ETRS89 / UTM zone 30N
    '25831',  # ETRS89 / UTM zone 31N
]
EPSG_DEFAULT = '25830'

CADASTRAL_REF_LEN = 14

GML_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<!-- Parcela Catastral para entregar a la D.G. del Catastro -->
<FeatureCollection
  xmlns:gml="http://www.opengis.net/gml/3.2"
  xmlns:gmd="http://www.isotc211.org/2005/gmd"
  xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:cp="http://inspire.ec.europa.eu/schemas/cp/4.0"
  xmlns:base="urn:x-inspire:specification:gmlas:BaseTypes:3.2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd http://inspire.ec.europa.eu/schemas/cp/4.0 http://inspire.ec.europa.eu/schemas/cp/4.0/CadastralParcels.xsd"
  xmlns="http://www.opengis.net/wfs/2.0"
  numberMatched="1"
  numberReturned="1"
  id="%(namespace)s"
>
%(features)s
<!-- Si se desea entregar varias parcelas en un mismo fichero, se pondrá un nuevo featureMember para cada parcela -->
</FeatureCollection>"""

GML_FEATURE = """   <member>
      <cp:CadastralParcel gml:id="%(namespace)s.%(label)s">
<!-- Superficie de la parcela en metros cuadrados. Tiene que coincidir con la calculada con las coordenadas.-->
         <cp:areaValue uom="m2">%(area)s</cp:areaValue>
         <cp:beginLifespanVersion xsi:nil="true" nilReason="http://inspire.ec.europa.eu/codelist/VoidReasonValue/Unpopulated"></cp:beginLifespanVersion>
         <cp:endLifespanVersion xsi:nil="true" nilReason="http://inspire.ec.europa.eu/codelist/VoidReasonValue/Unpopulated"></cp:endLifespanVersion>
<!-- Geometría en formato GML -->
         <cp:geometry><!-- srs Name código del sistema de referencia en el que se dan las coordenadas, que debe coincidir con el de la cartografía catastral -->
           <gml:MultiSurface gml:id="MultiSurface_%(namespace)s.%(label)s" srsName="http://www.opengis.net/def/crs/EPSG/0/%(epsg)s">
             <gml:surfaceMember>
               <gml:Surface gml:id="Surface_%(namespace)s.%(label)s" srsName="http://www.opengis.net/def/crs/EPSG/0/%(epsg)s">
                  <gml:patches>
                    <gml:PolygonPatch>
                      <gml:exterior>
                        <gml:LinearRing>
<!-- Lista de coordenadas separadas por espacios o en líneas diferentes -->
                          <gml:posList srsDimension="2" count="%(len_coords)s">%(coords)s
                          </gml:posList>
                        </gml:LinearRing>
                      </gml:exterior>
                    </gml:PolygonPatch>
                  </gml:patches>
                </gml:Surface>
              </gml:surfaceMember>
            </gml:MultiSurface>
         </cp:geometry>
         <cp:inspireId xmlns:base="http://inspire.ec.europa.eu/schemas/base/3.3">
<!-- Identificativo local de la parcela. Sólo puede tener letras y números. Se recomienda (pero no es necesario) poner siempre un dígito de control, por ejemplo utilizando el algoritmo del NIF -->
           <base:Identifier>
             <base:localId>%(label)s</base:localId>
             <base:namespace>%(base_namespace)s</base:namespace>
           </base:Identifier>
         </cp:inspireId>
         <cp:label/>
<!-- Siempre en blanco, ya que todavía no ha sido dada de alta en las bases de datos catastrales -->
         <cp:nationalCadastralReference>%(cadastral_reference)s</cp:nationalCadastralReference>
      </cp:CadastralParcel>
   </member>
"""


def dxf2gml(dxf_file, code):
    """
    Transforma la información de la geometría de un archivo DXF
    al estándar de Catastro en formato GML.

    dxf_file: Archivo en formato DXF con la geometría de origen
    code: Sistema de Referencia de Coordenadas del DXF (código EPSG)
    """

    if code not in EPSG_ZONES:
        return (
            False,
            f'Error: El código EPSG "{code}" es incorrecto'
        )

    namespace = ''
    features = ''

    driver = ogr.GetDriverByName('DXF')
    data_source = driver.Open(dxf_file, 0)

    layer = data_source.GetLayer()
    info = []
    for feature in layer:
        data = json.loads(feature.ExportToJson())
        reference = data["properties"]["Layer"]

        geom = feature.GetGeometryRef()
        area = geom.Area()

        if len(reference) == CADASTRAL_REF_LEN:
            cadastral_reference = reference
            if namespace == '':
                namespace = "ES.SDGC.CP"
                base_namespace = namespace
            elif namespace != "ES.SDGC.CP":
                return (
                    False,
                    "Error: Todas las parcelas deben tener Referencia Catastral"
                )
        else:
            cadastral_reference = ''
            if namespace == '':
                namespace = "ES.LOCAL"
                base_namespace = f"{namespace}.CP"
            elif namespace != "ES.LOCAL":
                return (
                    False,
                    "Error: Todas las parcelas deben tener Referencia Local"
                )

        if data["properties"]["Text"] == "SOLID":
            info.append(f'Referencia: {reference}, ({area:.4f} m^2)')

            perimeter = geom.GetGeometryRef(0)
            coords = ''
            len_coords = 0
            for i in range(0, perimeter.GetPointCount()):
                pt = perimeter.GetPoint(i)
                coords += f"\n{pt[0]} {pt[1]}"
                len_coords += 1

            features += GML_FEATURE % {
                "epsg": code,
                "namespace": namespace,
                "base_namespace": base_namespace,
                "area": area,
                "len_coords": len_coords,
                "coords": coords,
                "label": reference,
                "cadastral_reference": cadastral_reference
            }
        else:
            info.append(f'Referencia: {reference}. AVISO: Se ha encontrado una geometría no sólida')

    return (
        True,
        {
            'info': info,
            'gml': GML_TEMPLATE % {
                'namespace': namespace,
                'features': features
            }
        }
    )


def save_gml(dxf_file, code):
    print(f'\nProcesando fichero: {dxf_file}')

    ret, output = dxf2gml(dxf_file, code)
    if not ret:
        print(output)
        print(f'Error: fichero "{dxf_file}" no convertido!!!')
        return False

    gml_file, _ = os.path.splitext(dxf_file)
    gml_file += '.gml'
    with open(gml_file, 'w') as f:
        f.writelines(output['gml'].encode('utf-8'))

    for i in output['info']:
        print(i)

    print(f'Fichero generado: {gml_file}')

    return True


def usage():
    print('\nEjemplos de uso:')

    print('\n  Generar un fichero GML:')
    print('\t$ dxf2gml parcel1.dxf')

    print('\n  Generar un fichero GML con un determinado código EPSG:')
    print('\t$ dxf2gml parcel1.dxf 25831')

    print('\n  Generar un fichero GML por cada fichero DXF de un directorio:')
    print('\t$ dxf2gml directorio')


def main():
    if len(sys.argv) < 2:
        print('Error: parámetros insuficientes')
        usage()
        sys.exit(1)

    path = sys.argv[1]  # File or Directory Source
    epsg = EPSG_DEFAULT
    if len(sys.argv) == 3:
        epsg = sys.argv[2]

    if os.path.isfile(path):
        ret = save_gml(path, epsg)
        if not ret:
            sys.exit(1)
    elif os.path.isdir(path):
        ret = True
        for _file in glob.glob(os.path.join(path, '*.dxf')):
            ret = ret and save_gml(_file, epsg)
        if not ret:
            sys.exit(1)
    else:
        print(f'Error: No se ha encontrado el fichero o directorio "{path}"')
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
