import arcpy
from webhdfs import WebHDFS

inputFile = arcpy.GetParameterAsText(0)
hostname =arcpy.GetParameterAsText(1)
port =arcpy.GetParameterAsText(2)
username =arcpy.GetParameterAsText(3)
hdfsRemoteFile =arcpy.GetParameterAsText(4)
hdfsAppend =arcpy.GetParameter(5)

webHDFS = WebHDFS(hostname, int(port),username)
webHDFS.copyToHDFS(inputFile, hdfsRemoteFile)

