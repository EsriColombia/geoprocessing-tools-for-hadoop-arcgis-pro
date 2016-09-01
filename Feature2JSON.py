import sys
import arcpy
from JSONUtil import ConvertFC2JSON,ConvertFC2JSONUnenclosed

inputFC = arcpy.GetParameterAsText(0)
outputJSON = arcpy.GetParameterAsText(1)
JSON_Type =arcpy.GetParameterAsText(2)
isFormatted =arcpy.GetParameter(3)


try:
    print ("JSON_Type")
    arcpy.AddMessage(JSON_Type)

    f = open(outputJSON, 'w')

    if(JSON_Type=="ENCLOSED_JSON"):
        ConvertFC2JSON(inputFC,f,isFormatted)
    else:
        ConvertFC2JSONUnenclosed(inputFC,f,isFormatted)
        
    f.close()
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0]) 
