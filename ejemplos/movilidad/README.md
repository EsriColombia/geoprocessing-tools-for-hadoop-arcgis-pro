## Movilidad

En este escenario se describe la integraci�n de informaci�n desde el SIG hacia la infraestructura Hortonworks. En este escenario para realizar las operaciones espaciales usando Hive se cuenta con:

* Unidad Administrativa: Se refiere al feature class de Barrios, el cual se requiere para realizar las agregaciones.
* Herramientas para la conversi�n de datos a formato JSON (formato soportado de forma nativa por Hive)
* Modelo de Geoprocesamiento para que usando ArcGIS Pro, automatizar los procesos e integrar las herramientas.

# Copiar FeatureClass a HDFS

![](img/01.JPG)

Como parte de la integraci�n hacia Hadoop las herramientas permiten desde ArcGIS Pro, realizar la conversi�n de Informaci�n desde un formato geogr�fico (FeatureClass) a un formato JSON, el cual puede ser utilizado en Hadoop para ser procesado.  Siga los siguientes pasos para realizar la transformaci�n y copiado del Feature Class Barrio.

1. Para realizar el copiado, previamente debe existir la carpeta donde reposar� la informaci�n.  En al caso que no extista deber� ejecutar los siguientes comando por consola en el nodo de Hadoop:

 		#Crear la carpeta si es necesario.
 		hadoop fs -mkdir movilidad
        hadoop fs -mkdir movilidad/data
        
2. Utilizando la Caja de Herramientas BigData.tbx, ejecute el modelo "FC2JSON2HDFS (Movilidad)"

 ![](img/02.JPG)

 Especifique los par�metros:

	[FC]: Feature Class que ser� transformado a JSON.
	Barrios.json: Archivo JSON resultado de la transformaci�n a formato JSON.
	HDFS Server Hostname: sandbox.hortonworks.com.
	HDFS TCP Port Number: 50070.
	HDFS Username: root.
	HDFS Remote File: /user/root/movilidad/data/Barrios.json. 



