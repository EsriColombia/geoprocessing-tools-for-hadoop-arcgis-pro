#
import arcpy
from OozieUtil import Configuration,Oozie,OozieError

urlOzie = arcpy.GetParameterAsText(0)
properties =arcpy.GetParameterAsText(1)

if __name__ == '__main__':      
    try:
        conf = Configuration(properties)
    
        # Create Oozie client        
        oozieClient = Oozie(urlOzie)
        # Submit Job
        
        jobID = oozieClient.submit(conf.xmldata)
        arcpy.AddMessage("jobID: {}".format(jobID))
        oozieClient.run(jobID)
    except OozieError as err:
        arcpy.AddMessage (str(err))
    except:
        for ei in sys.exc_info() :
            if isinstance(ei, Exception) :
                arcpy.AddMessage (str(ei))

