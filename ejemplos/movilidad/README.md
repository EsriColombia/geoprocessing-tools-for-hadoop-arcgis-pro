## Movilidad

En este escenario se describe la integración de información desde el SIG hacia la infraestructura Hortonworks. En este escenario para realizar las operaciones espaciales usando Hive se cuenta con:

* Unidad Administrativa: Se refiere al feature class de Barrios, el cual se requiere para realizar las agregaciones.
* Herramientas para la conversión de datos a formato JSON (formato soportado de forma nativa por Hive)
* Modelo de Geoprocesamiento para que usando ArcGIS Pro, automatizar los procesos e integrar las herramientas.

# Copiar FeatureClass a HDFS

![](img/01.JPG)

Como parte de la integración hacia Hadoop las herramientas permiten desde ArcGIS Pro, realizar la conversión de Información desde un formato geográfico (FeatureClass) a un formato JSON, el cual puede ser utilizado en Hadoop para ser procesado.  Siga los siguientes pasos para realizar la transformación y copiado del Feature Class Barrio.

1. Para realizar el copiado, previamente debe existir la carpeta donde reposará la información.  En al caso que no extista deberá ejecutar los siguientes comando por consola en el nodo de Hadoop:

 		#Crear la carpeta si es necesario.
 		hadoop fs -mkdir movilidad
        hadoop fs -mkdir movilidad/data
        
2. Utilizando la Caja de Herramientas BigData.tbx, ejecute el modelo "FC2JSON2HDFS (Movilidad)"

 ![](img/02.JPG)

 Especifique los parámetros:

	[FC]: Feature Class que será transformado a JSON.
	Barrios.json: Archivo JSON resultado de la transformación a formato JSON.
	HDFS Server Hostname: sandbox.hortonworks.com.
	HDFS TCP Port Number: 50070.
	HDFS Username: root.
	HDFS Remote File: /user/root/movilidad/data/Barrios.json. 



