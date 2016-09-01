# Ejemplo 1. Agregación
En este ejemplo se tienen en cuenta datos de recorridos de vehiculos en un intervalo de tiempo definido. 


Cree un directorio en Hadoop

```bash
hadoop fs -mkdir movilidad-demo
```

Copie los archivos de ejemplo a HDFS usando el comando siguiente desde la consola.

hadoop fs -put /ruta/en/sistemalocal /path/to/hdfs
```bash
hadoop fs -put gis-hadoop/datos movilidad-demo
```
Verifique que esten los archivos:
```bash
hadoop fs -ls movilidad-demo
```

Inicie la consola de comandos Hive.

> **Note**: Si tiene algun problema con Hive vea [aqui](https://github.com/Esri/spatial-framework-for-hadoop/wiki/ST_Geometry-for-Hive-Compatibility-with-Hive-Versions) la lista completa de las compatibilidades con ST_Geometry.

```bash
# use '-S' para modo silencioso
hive
```

> Este ejemplo asume que Hive esta instalado en un cluster Local. Si usted esta usando un cluster remoto, necesitará mover los archivos a HDFS y cambiar la tabla de definiciones como sea requerido.

Adicione las librerias externas requeridas para la creacion de las funciones temporales para los llamados del API.
```bash
add jar
  ${env:HOME}/esri-git/gis-tools-for-hadoop/samples/lib/esri-geometry-api.jar
  ${env:HOME}/esri-git/gis-tools-for-hadoop/samples/lib/spatial-sdk-hadoop.jar;
create temporary function ST_Bin as 'com.esri.hadoop.hive.ST_Bin';
create temporary function ST_Point as 'com.esri.hadoop.hive.ST_Point';
create temporary function ST_BinEnvelope as 'com.esri.hadoop.hive.ST_BinEnvelope';
create temporary function ST_Contains as 'com.esri.hadoop.hive.ST_Contains';

```

> Esta es una implementacion mínima de funciones ST_Geometry que se encuentran en [Hive Spatial Library](https://github.com/Esri/spatial-framework-for-hadoop/wiki/Hive-Spatial).  El listado de funciones disponibles en [linked repository](https://github.com/Esri/spatial-framework-for-hadoop/wiki/UDF-Documentation).

Elimine la tabla M01:
```bash
drop table M01;
```
Defina el esque para para la creacion de la tabla.  Los datos estan almacenados en formato CSV (valores separados por coma), el cual esta soportado por Hive de forma Nativa.


```sql
CREATE TABLE m01 (id string,booking_id string,driver_id string,created_at string,latitude DOUBLE,longitude DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

Cargue los datos en la tabla:
```sql
LOAD DATA INPATH 'movilidad/data/M01.csv' OVERWRITE INTO TABLE M01; 
```

Cree la tabla donde se almacenará el resultado del análisis.

Elimine la tabla de resultados de existir:
```sql
DROP TABLE agg_res;
```

```sql
CREATE TABLE agg_res(area binary, count double)
ROW FORMAT SERDE 'com.esri.hadoop.hive.serde.JsonSerde'              
STORED AS INPUTFORMAT 'com.esri.json.hadoop.EnclosedJsonInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat';
```


Ejecute el Análisis:
```sql
FROM (SELECT ST_Bin(0.001, ST_Point(longitude, latitude)) bin_id, * FROM m01) bins
INSERT OVERWRITE TABLE agg_res
SELECT ST_BinEnvelope(0.001, bin_id) shape, count(*) count
GROUP BY bin_id;
```