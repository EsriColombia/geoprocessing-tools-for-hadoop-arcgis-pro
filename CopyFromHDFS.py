import arcpy,shutil,sys,tempfile
import os
from webhdfs import WebHDFS

hostname = arcpy.GetParameterAsText(0)
port =arcpy.GetParameterAsText(1)
username =arcpy.GetParameterAsText(2)
webhdfs_file_name =arcpy.GetParameterAsText(3)
out_local_file_name =arcpy.GetParameterAsText(4)

try :
    wh = WebHDFS(hostname, int(port),username)
    fs = wh.getFileStatus(webhdfs_file_name)
    if fs['type'] == 'FILE':
        wh.copyFromHDFS(webhdfs_file_name, out_local_file_name, overwrite = bool(arcpy.gp.overwriteOutput))
    else: #DIRECTORY - copy all non-empty files from the directory (non-recursively) and append to the output file with NL
        temp_file = tempfile.NamedTemporaryFile(delete = False)
        temp_file_name = temp_file.name
        temp_file.close()
        
        with open(out_local_file_name, "wb") as out_local_file:
            file_list = wh.listDirEx(webhdfs_file_name)
            for file in file_list:
                if file['length'] != 0 :
                    wh.copyFromHDFS(webhdfs_file_name + '/' + file['pathSuffix'], temp_file_name, overwrite = True)
                    temp_file = open(temp_file_name, "rb")
                    shutil.copyfileobj(temp_file, out_local_file, length = 1024 * 1024)
                    temp_file.close()
        os.remove(temp_file_name)

    
except Exception:
    e = sys.exc_info()[1]
    arcpy.AddMessage(e.args[0]) 




