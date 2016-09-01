# Aggregation Sample for Hive
Make sure you are in the git folder - if you just came from the beginner tutorial, it will look like this: `[root@sandbox esri-git]#`.

Make an earthquake demo directory in hadoop
```bash
hadoop fs -mkdir earthquake-demo
```

hadoop fs -put /path/on/localsystem /path/to/hdf
```bash
hadoop fs -put gis-tools-for-hadoop/samples/data/counties-data earthquake-demo
hadoop fs -put gis-tools-for-hadoop/samples/data/earthquake-data earthquake-demo
```
Check that it worked:
```bash
hadoop fs -ls earthquake-demo
```

Start the Hive Command line (Hive CLI).  If you do not have Hive installed, see [Hive Installation](https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-InstallationandConfiguration) - this sample requires Hive 0.10.0 or above (or Hive 0.9.0 patched with [HIVE-2736](https://issues.apache.org/jira/browse/HIVE-2736)). 

> **Note**: If you are having issues with Hive - See [here](https://github.com/Esri/spatial-framework-for-hadoop/wiki/ST_Geometry-for-Hive-Compatibility-with-Hive-Versions) for a complete list of hive compatibilities with ST_Geoemtry.

```bash
# use '-S' for silent mode
hive
```

> This sample assumes that Hive is installed on a local cluster.  If you are using a remote cluster, you will need to move your files to HDFS and change table definitions as needed.

Add the required external libraries and create temporary functions for the geometry api calls.
```bash
add jar
  ${env:HOME}/esri-git/gis-tools-for-hadoop/samples/lib/esri-geometry-api.jar
  ${env:HOME}/esri-git/gis-tools-for-hadoop/samples/lib/spatial-sdk-hadoop.jar;
  
create temporary function ST_Point as 'com.esri.hadoop.hive.ST_Point';
create temporary function ST_Contains as 'com.esri.hadoop.hive.ST_Contains';
```

> This is a minimum implementation the ST_Geometry user defined functions found in the [Hive Spatial Library](https://github.com/Esri/spatial-framework-for-hadoop/wiki/Hive-Spatial).  The full list of functions is available in the [linked repository](https://github.com/Esri/spatial-framework-for-hadoop/wiki/UDF-Documentation).

Drop the tables named counties and earthquakes:
```bash
drop table earthquakes;
drop table counties;
```
Define a schema for the [earthquake data](https://github.com/Esri/gis-tools-for-hadoop/tree/master/samples/data/earthquake-data).  The earthquake data is in CSV (comma-separated values) format, which is natively supported by Hive.

```sql
CREATE TABLE earthquakes (earthquake_date STRING, latitude DOUBLE, longitude DOUBLE, depth DOUBLE, magnitude DOUBLE,
    magtype string, mbstations string, gap string, distance string, rms string, source string, eventid string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

Define a schema for the [California counties data](https://github.com/Esri/gis-tools-for-hadoop/tree/master/samples/data/counties-data).  The counties data is stored as [Enclosed JSON](https://github.com/Esri/spatial-framework-for-hadoop/wiki/JSON-Formats).  

```sql
CREATE TABLE counties (Area string, Perimeter string, State string, County string, Name string, BoundaryShape binary)                                         
ROW FORMAT SERDE 'com.esri.hadoop.hive.serde.JsonSerde'              
STORED AS INPUTFORMAT 'com.esri.json.hadoop.EnclosedJsonInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat';
```

Load data into the respective tables:
```sql
LOAD DATA INPATH 'earthquake-demo/earthquake-data/earthquakes.csv' OVERWRITE INTO TABLE earthquakes;
LOAD DATA INPATH 'earthquake-demo/counties-data/california-counties.json' OVERWRITE INTO TABLE counties;
```

Run the demo analysis:

```sql
SELECT counties.name, count(*) cnt FROM counties
JOIN earthquakes
WHERE ST_Contains(counties.boundaryshape, ST_Point(earthquakes.longitude, earthquakes.latitude))
GROUP BY counties.name
ORDER BY cnt desc;
```

Your results should look like this:

```
Kern  36
San Bernardino	35
Imperial	28
Inyo	20
Los Angeles	18
Riverside	14
Monterey	14
Santa Clara	12
Fresno	11
San Benito	11
San Diego	7
Santa Cruz	5
San Luis Obispo	3
Ventura	3
Orange	2
San Mateo	1
```

===

## run-sample.sql

Alternatively, you can run the entire sample using `run-sample.sql`.

First move to the Hive sample directory and run Hive.

```bash
cd ~/esri-git/gis-tools-for-hadoop/samples/point-in-polygon-aggregation-hive
hive -S
```

Now run the sample sql file from within Hive

```bash
source run-sample.sql;
```



## Agregaci�n de puntos Hive
Estos ejemplos son proporcionados como regerencia para la construcci�n de herramientas espaciales que realizan operaciones en hive.	

```bash

hadoop fs -mkdir earthquake-demo

```

> **Note**: If you are having issues with Hive - See [here](

> This sample assumes that Hive is installed on a local cluster.  If you are using a remote cluster, you will need to move your files to HDFS and change table definitions as needed.
- 

```sql

SQL

```

```
Kern  36

```

===
