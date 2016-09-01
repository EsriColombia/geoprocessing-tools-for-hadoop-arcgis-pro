import sys
from JSONUtil import ConvertJSONToFCUnenclosed,ConvertJSONToFC

inputJSON = arcpy.GetParameterAsText(0)
outputFC = arcpy.GetParameterAsText(1)
JSON_Type =arcpy.GetParameterAsText(2)

f = open(inputJSON, 'r')
try:
    if(JSON_Type=="ENCLOSED_JSON"):
        ConvertJSONToFC(f,outputFC)
    else:
        ConvertJSONToFCUnenclosed(f,outputFC)   
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0]) 

