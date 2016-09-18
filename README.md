# geoprocessing-tools-for-hadoop-arcgis-pro
El __Geoprocessing Tools for Hadoop (ArcGIS Pro)__ proporciona herramientas para ayudar con la integración con Hadoop. Específicamente las herramientas permiten:

* Permite el intercambio de datos entre una [ArcGIS Geodatabase](http://resources.arcgis.com/en/help/main/10.2/index.html#/What_is_a_geodatabase/003n00000001000000/) y un Sistema Hadoop, y  
* Permite a los usuarios de ArcGIS ejecutar Jobs.

## Elementos

* Herramientas para convertir entre Feature Classes en una Geodatabase y archivos JSON formateado.
* Herramientas que copian archivos desde ArcGIS a Hadoop y viceversa.
* Herramientas para ejecutar un flujo de trabajo [Oozie](http://oozie.apache.org/) en Hadoop, y verificar el estado del flujo de trabajo.

## Referencias.

* [Wiki](https://github.com/EsriColombia/geoprocessing-tools-for-hadoop-arcgis-pro/wiki) de herramientas de geoprocesamiento para ArcGIS Pro.
* [Wiki](https://github.com/Esri/geoprocessing-tools-for-hadoop/wiki) de herramientas de geoprocesamiento para ArcMap disponibles.
* [Tutoriales](https://github.com/Esri/gis-tools-for-hadoop/wiki) on how to run the geoprocessing tools.

## Instrucciones
1. Descargar este repositorio como un archivo .zip y descomprimalo en la ubicación que desee o clone el repositorio con una herramienta git.
2. Acceder a la Caja de herramientas de [ArcGIS Pro](http://www.esri.com/en/software/arcgis-pro), 
3. Use las herramientas individualmente, o uselas en modelos o scripts python.

## Requirements

* ArcGIS Pro 1.3 o superior.
* Un sistema Hadoop con soporte WebHDFS.

## Dependencies
* WebHDFS que reside en la carpeta de la herramienta.
* La librería de Python webhdfs-py es requerida para soporte WebHDFS.
* La librería de Python Requests es requerida para OozieUtils.py 

## Recursos

* [GeoData Blog en ArcGIS](http://blogs.esri.com/esri/arcgis/author/jonmurphy/)
* [Big Data Place en GeoNet](https://geonet.esri.com/groups/big-data)
* [Centro de Recursos ArcGIS Geodata]( http://resources.arcgis.com/en/communities/geodata/)
* [ArcGIS Blog](http://blogs.esri.com/esri/arcgis/)
* [twitter@esri](http://twitter.com/esri)

## Issues

Por favor haganos saber si encuentra algún bug.

## Licensing
Copyright 2013-2016 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's 
[license.txt](https://raw.github.com/Esri/hadoop-gp-tools/master/license.txt) file.

[](Esri Tags: ArcGIS, Geoprocessing, GP, Hadoop, Spatial, Python)
[](Esri Language: Python)