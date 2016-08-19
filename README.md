# geoprocessing-tools-for-hadoop-arcgis-pro
The __Geoprocessing Tools for Hadoop (ArcGIS Pro)__ proporciona herramientas para ayudar con la integración con Hadoop. Específicamente las herramientas permiten:

* Permite el intercambio de datos entre una [ArcGIS Geodatabase](http://resources.arcgis.com/en/help/main/10.2/index.html#/What_is_a_geodatabase/003n00000001000000/) y un Sistema Hadoop, y  
* Permite a los usuarios de ArcGIS ejecutar Jobs.

## Elementos

* Herramientas para convertir entre Feature Classes en una Geodatabase y archivos JSON formateado.
* Herramientas que copian archivos desde ArcGIS a Hadoop y viceversa.
* Herramientas para ejecutar un flujo de trabajo [Oozie](http://oozie.apache.org/) en Hadoop, y verificar el estado del flujo de trabajo.

## Referencias.

* [Wiki](https://github.com/Esri/geoprocessing-tools-for-hadoop/wiki) de herramientas de geoprocesamiento disponibles.
* [Tutoriales](https://github.com/Esri/gis-tools-for-hadoop/wiki) on how to run the geoprocessing tools.

## Instrucciones
1. Descargar este repositorio como un archivo .zip y descomprimalo en la ubicación que desee o clone el repositorio con una herramienta git.
2.
3. In the ‘ArcToolbox’ pane of [ArcGIS Desktop](http://www.esri.com/software/arcgis/arcgis-for-desktop/), 
use the [‘Add Toolbox…’ command](http://resources.arcgis.com/en/help/main/10.2/index.html#//003q0000001m000000) 
to add the Hadoop Tools toolbox (the HadoopTools.pyt file you saved in step 1) file 
into ArcGIS Desktop.
4. Use the tools individually, or use them in models and scripts, such as the examples 
in: [GIS Tools for Hadoop](https://github.com/Esri/gis-tools-for-hadoop).

## Requirements

* ArcGIS Pro 1.3 o superior.
* Un sistema Hadoop con soporte WebHDFS.

## Dependencies
* WebHDFS and Requests are bundled-in and reside in the tool folder.
* A Python library webhdfs-py is required for WebHDFS support.  Source is located 
at [webhdfs-py](https://github.com/Esri/webhdfs-py).
* The Requests python library is required for OozieUtils.py (installation doc is located 
at http://docs.python-requests.org/en/latest/user/install/#install).

## Resources

* [GeoData Blog on the ArcGIS Blogs](http://blogs.esri.com/esri/arcgis/author/jonmurphy/)
* [Big Data Place on GeoNet](https://geonet.esri.com/groups/big-data)
* [ArcGIS Geodata Resource Center]( http://resources.arcgis.com/en/communities/geodata/)
* [ArcGIS Blog](http://blogs.esri.com/esri/arcgis/)
* [twitter@esri](http://twitter.com/esri)

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

## Contributing

Esri welcomes contributions from anyone and everyone. Please see our [guidelines for contributing](https://github.com/esri/contributing)

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