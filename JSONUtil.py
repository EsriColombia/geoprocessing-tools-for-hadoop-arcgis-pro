import os, sys, json, datetime, uuid
import arcpy

##################################################
def _createDataset(output_fc, json_fc, geomType = None, geomFieldName = None) :
    #create in_memory table/FC first to add fields faster then regular fgdb
    in_mem = 'in_memory'
    temp_name = 'tmp' + str(uuid.uuid1()).replace('-', '_')
    in_mem_fc = in_mem + '/' + temp_name
    
    if geomType :
        hasM = u'DISABLED'
        if u'hasM' in json_fc :
            hasM = ('ENABLED' if json_fc[u'hasM'] else 'DISABLED')
          
        hasZ = u'DISABLED'
        if u'hasZ' in json_fc :
            hasZ = ('ENABLED' if json_fc[u'hasZ'] else 'DISABLED')

        spRef = None
        if u'spatialReference' in json_fc :
            spRef = json_fc['spatialReference']
            if type(spRef) == dict :
                spRef = spRef[u'wkid']
        else:
            spRef = arcpy.SpatialReference(4326)
        arcpy.CreateFeatureclass_management(in_mem, temp_name, geomType, '', hasM, hasZ, spRef)
    else :
        arcpy.CreateTable_management(in_mem, temp_name)
        
    #add fields
    attributeFieldList = []
    for field in json_fc[u'fields'] :
        field_type = None
        if 'type' in field:
            field_type = field[u'type'][len('esriFieldType'):]
        else:
            field_type = 'TEXT'

        if field_type != 'OID' and field[u'name'] not in ['Shape_Length', 'Shape_Area', geomFieldName]:
            if field_type == u'String' :
                field_type = 'TEXT'
            arcpy.AddField_management(in_mem_fc, field[u'name'], field_type, "", "", (field[u'length'] if 'length' in field else ""), field[u'alias'], True)
            #keep original field list to access json attributes while inserting into new table (new table can have different field names after validation)
            attributeFieldList.append(field[u'name'])
            
    #copy table/fc to the destination workspace (helps with fields validation too. Validation is done inside Copy...)
    if geomType :
        arcpy.CopyFeatures_management(in_mem_fc, output_fc)
    else :
        arcpy.CopyRows_management(in_mem_fc, output_fc)

    arcpy.Delete_management(in_mem_fc)
    return attributeFieldList

##################################################
def _iterLoadUnenclosedJSON(json_file):
    buffer = u''
    dec = json.JSONDecoder(strict=False)
    while True :
        line = json_file.read(1024 * 4)
        #line = unicode(json_file.read(1024 * 4))
        if len(line) == 0 : 
            break;
        buffer += line.strip(u'\n\r\t')
        while True:
            try:
                r = dec.raw_decode(buffer)
            except:
                break
            yield r[0]
            buffer = buffer[r[1]:].strip(u'\n\r\t')

##################################################
def _getFCProps(feature) :
    json_fc = {u'fields' : []}

    # get geometry props
    geomType = None
    if u'geometry' in feature :
        geom = feature[u'geometry']
        if geom != None :
            if u'spatialReference' in geom :
                json_fc[u'spatialReference'] = geom[u'spatialReference']
            if u'z' in geom :
                json_fc[u'hasZ'] = True
            if u'm' in geom :
                json_fc[u'hasM'] = True
                
            if u'rings' in geom :
                geomType = u'esriGeometryPolygon'
            elif u'paths' in geom :
                geomType = u'esriGeometryPolyline'
            elif u'points' in geom :
                geomType = u'esriGeometryMultipoint'
            elif u'x' in geom :
                geomType = u'esriGeometryPoint'
            else :
                raise JUError('Unknown geometry type')

        json_fc[u'geometryType'] = geomType
        

    # get attribute props
    if u'attributes' in feature:
        attributes = feature[u'attributes']
        fields = json_fc[u'fields']
        for fld_name, fld_val in attributes.items() :
            field = {}
            field['name'] = fld_name
            field['alias'] = fld_name
            fld_type = type(fld_val)
            #if fld_type == str or fld_type == str:
            if fld_type == str or fld_type == str:
                date = None
                fmts = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d'] #TODO : support iso8601 string representation '%Y-%m-%dT%H:%M:%S.%f%z'
                for fmt in fmts:
                    try:
                        date = datetime.datetime.strptime(fld_val, fmt)
                        break
                    except:
                        pass
                
                if date is not None:
                    field['type'] = 'esriFieldTypeDate'
                else:
                    field['type'] = 'esriFieldTypeString'

            elif fld_type == int or  fld_type == int:
                if fld_name == 'OBJECTID' or fld_name == 'OID' or fld_name == 'FID' :
                    field['type'] = 'esriFieldTypeOID'
                else :
                    field['type'] = 'esriFieldTypeInteger'
            elif fld_type == float:
                field['type'] = 'esriFieldTypeDouble'
            elif fld_type == datetime.datetime:
                field['type'] = 'esriFieldTypeDate'
            fields.append(field)
            
    return json_fc

##################################################
def _getGeometryType(json_fc) :
    geomType = None
    try :
        if u'geometryType' in json_fc : 
            geomType = {'esriGeometryPolygon'    : 'POLYGON',
                        'esriGeometryPolyline'   : 'POLYLINE',
                        'esriGeometryMultipoint' : 'MULTIPOINT',
                        'esriGeometryPoint'      : 'POINT'}[json_fc[u'geometryType']]
    except :
        geomType = 'POINT'
        
    return geomType

##################################################
def _getEsriGeometryType(geom_type) :
    esriGeomType = None
    try :
        esriGeomType = {'Polygon'    : 'esriGeometryPolygon',
                        'Polyline'   : 'esriGeometryPolyline',
                        'MultiPoint' : 'esriGeometryMultipoint',
                        'Point'      : 'esriGeometryPoint'}[geom_type]
    except :
        esriGeomType = 'POINT'
        
    return esriGeomType

##################################################
def _getEmptyGeom(geomType) :
    if geomType == 'POINT' :
        return u'{"x" : null}'
    if geomType == 'MULTIPOINT' :
        return u'{"points" : [  ]}'
    if geomType == 'POLYLINE' :
        return u'{"paths" : [ ]}'
    if geomType == 'POLYGON' :
        return u'{"rings" : [ ]}'
    raise JUError('Unknown geometry type')

##################################################
def ConvertJSONToFCUnenclosed(json_file, output_fc) :
    json_fc = {}
    
    # guess feature class properties from json record
    for feature in _iterLoadUnenclosedJSON(json_file) :
        if 'fields' in feature :
            raise JUError(json_file.name + ' is not an unenclosed JSON')
        
        json_fc = _getFCProps(feature)
        if u'geometryType' in json_fc and json_fc[u'geometryType'] == None: 
            continue
        break
    json_file.seek(0)

    geomType = _getGeometryType(json_fc)

    #create output dataset
    attributeFieldList = _createDataset(output_fc, json_fc, geomType)
    if arcpy.Exists(output_fc) == False :
        raise JUError('Cannot create: ' + output_fc)
    
    #prepare new field list for insert cursor
    field_list = []
    desc_output_fc = arcpy.Describe(output_fc)
    output_fields = desc_output_fc.fields
    
    for field in output_fields :
        if field.type not in ['Geometry', 'OID'] and field.name not in ['Shape_Length', 'Shape_Area']:
            field_list.append(str(field.name))

    #insert features
    try :
        if geomType :
            geomEmpty = _getEmptyGeom(geomType)
            
        with arcpy.da.InsertCursor(output_fc, field_list + ([u'shape@json'] if geomType else [])) as cursor:
            for feature in _iterLoadUnenclosedJSON(json_file) :
                row = []
                for field in attributeFieldList :
                    row.append(feature[u'attributes'][field])
                    
                if geomType :
                    geom = str(json.dumps(feature[u'geometry']))
                    if geom == 'null' :
                        geom = geomEmpty
                    row.append(geom)
                    
                cursor.insertRow(row)
    except :  
        raise JUError('Cannot save: ' + output_fc)

    return

##################################################
def ConvertJSONToFC(json_file, output_fc) :
    json_fc = json.load(json_file)
    
    workspace = os.path.dirname(output_fc)
    fc_name = os.path.basename(output_fc)
    
    geomType = _getGeometryType(json_fc)
        
    #create output dataset
    attributeFieldList = _createDataset(output_fc, json_fc, geomType)
    if arcpy.Exists(output_fc) == False :
        raise JUError('Cannot create: ' + output_fc)
    
    #prepare new field list for insert cursor
    field_list = []
    field_list_date = []
    desc_output_fc = arcpy.Describe(output_fc)
    output_fields = desc_output_fc.fields
    
    for field in output_fields :
        if field.type not in ['Geometry', 'OID'] and field.name not in ['Shape_Length', 'Shape_Area']:
            field_list.append(str(field.name))
        if field.type == 'Date':
            field_list_date.append(str(field.name))
    
    #insert features
    try :
        if geomType :
            geomEmpty = _getEmptyGeom(geomType)
            
        with arcpy.da.InsertCursor(output_fc, field_list + ([u'shape@json'] if geomType else [])) as cursor:
            for feature in json_fc[u'features'] :
                row = []
                for field in attributeFieldList :
                    
                    attr = feature[u'attributes'][field]
                    
                    # convert JSDate integer to string
                    if (type(attr) == int or type(attr) == int) and (field in field_list_date):
                        attr = datetime.datetime.utcfromtimestamp(float(attr) / 1000.)
                    row.append(attr)
                    
                if geomType :
                    geom = str(json.dumps(feature[u'geometry']))
                    if geom == 'null' :
                        geom = geomEmpty
                    row.append(geom)
                    
                cursor.insertRow(row)
    except :    
        raise JUError('Cannot save: ' + output_fc)

##################################################
def _dumpFields2JSONStr(fields, pjson = False) :
    fields_json = []
    for field in fields :
        field_type = field.type
        if field_type not in ['Geometry', 'OID'] and field.name not in ['Shape_Length', 'Shape_Area']:
            field_json = {}
            field_json[u'alias'] = str(field.aliasName)
            field_json[u'name'] = str(field.name)
            field_json[u'type'] = str('esriFieldType' + field_type)
            if field_type in ['String', 'Blob'] :
                field_json[u'length'] = field.length          
            
            fields_json.append(field_json)
        
    return str(json.dumps(fields_json, indent = (4 if pjson else None)))

##################################################
def ConvertFC2JSON(fc, ftmp, pjson = False) :
    arcpy.AddMessage("\n")
    arcpy.AddMessage("ConvertFC2JSON")
    arcpy.AddMessage("\n")
    arcpy.AddMessage("ftmp: {}".format(ftmp))
    
    desc_fc = arcpy.Describe(fc)
    feature_type = None
    shape_type = None
    try :
        feature_type = desc_fc.featureType
        shape_type = _getEsriGeometryType(desc_fc.shapeType)
    except :
        pass

    NL = u''
    if pjson == True:
        NL = u'\n'
        
    ftmp.write(u'{' + NL)

    arcpy.AddMessage("\n")
    arcpy.AddMessage("desc_fc{}".format(desc_fc))
    arcpy.AddMessage("\n")
    arcpy.AddMessage("feature_type{}".format(feature_type))
    
    #add fields
    fields = desc_fc.fields
    fields_json_string = _dumpFields2JSONStr(fields, pjson)

    fields_json_string

    arcpy.AddMessage("\n")
    arcpy.AddMessage("fields_json_string: {}".format(fields_json_string))
    
    ftmp.write(u'"fields": ' + fields_json_string + u',' + NL)
    
    #add Z, M info
    if feature_type :
        ftmp.write(u'"geometryType" : "{0}",'.format(shape_type) + NL)
        ftmp.write(u'"hasZ": {0},'.format(u'true' if desc_fc.hasZ else u'false') + NL)
        ftmp.write(u'"hasM": {0},'.format(u'true' if desc_fc.hasM else u'false') + NL)
        ftmp.write(u'"spatialReference": {{"wkid":{0}}},'.format(desc_fc.spatialReference.factoryCode) + NL)
               
    #prepare field list
    field_list = []
    shape_field = None
    if feature_type :
        shape_field = str(desc_fc.shapeFieldName)
    
    for field in fields :
        if field.type not in ['Geometry', 'OID'] and field.name not in ['Shape_Length', 'Shape_Area']:
            field_list.append(str(field.name))

    if feature_type :
        field_list.append(u'shape@json')
    arcpy.AddMessage("\n")
    arcpy.AddMessage("field_list{}".format(field_list))
    #add fieatures
    ftmp.write(u'"features": [' + NL)
    with arcpy.da.SearchCursor(fc, field_list) as cursor:
        add_comma = False
        row_len_no_geom = len(field_list) - (1 if feature_type else 0) #process geometry separately
        attributes_json = {}

        for row in cursor :
            attributes_json.clear()
            i = 0
            for attr in row :
                if i < row_len_no_geom :
                    attributes_json[field_list[i]] = (attr if type(attr) != datetime.datetime else str(attr))
                    i += 1

            if add_comma :
                ftmp.write(u',' + NL)
            else:
                add_comma = True

            attributes_str = str(json.dumps(attributes_json, indent = (4 if pjson else None)))
            if feature_type :    
                geometry_str = str(row[len(row) - 1]) if pjson != True else str(json.dumps(json.loads(row[len(row) - 1]), indent=4))
                row_json_str = u'{{{2}"attributes": {0},{3}"geometry": {1}{4}}}'.format(attributes_str, geometry_str, NL, NL, NL)
            else:
                row_json_str = u'{{{1}"attributes": {0}{2}}}'.format(attributes_str, NL, NL)

            ftmp.write(row_json_str)
            
    ftmp.write(u']' + NL)

    ftmp.write(u'}')
    
##################################################
def ConvertFC2JSONUnenclosed(fc, ftmp, pjson = False) :
    arcpy.AddMessage("\n")
    arcpy.AddMessage("ConvertFC2JSONUnenclosed")
    desc_fc = arcpy.Describe(fc)
    feature_type = None
    try :
        feature_type = desc_fc.featureType
    except :
        pass
    arcpy.AddMessage("\n")
    arcpy.AddMessage("desc_fc{}".format(desc_fc))
    arcpy.AddMessage("\n")
    arcpy.AddMessage("feature_type{}".format(feature_type))
    NL = u''
    if pjson == True:
        NL = u'\n'
    
    #prepare field list
    field_list = []
    shape_field = None
    if feature_type :
        shape_field = str(desc_fc.shapeFieldName)
    
    for field in desc_fc.fields :
        if field.type not in ['Geometry', 'OID'] and field.name not in ['Shape_Length', 'Shape_Area']:
            field_list.append(str(field.name))

    if feature_type :
        field_list.append(u'shape@json')

    arcpy.AddMessage("\n")
    arcpy.AddMessage("field_list{}".format(field_list))
    
    
    #add fieatures
    with arcpy.da.SearchCursor(fc, field_list) as cursor:
        
        row_len_no_geom = len(field_list) - (1 if feature_type else 0) #process geometry separately
        attributes_json = {}

        arcpy.AddMessage("\n")
        arcpy.AddMessage("row_len_no_geom {}".format(row_len_no_geom))
        
        for row in cursor :
            attributes_json.clear()
            i = 0
            for attr in row :
                if i < row_len_no_geom :
                    attributes_json[field_list[i]] = (attr if type(attr) != datetime.datetime else str(attr))
                    i += 1

            attributes_str = str(json.dumps(attributes_json, indent = (4 if pjson else None)))
            if feature_type :    
                geometry_str = str(row[len(row) - 1]) if pjson != True else str(json.dumps(json.loads(row[len(row) - 1]), indent=4))
                row_json_str = u'{{{2}"attributes": {0},{3}"geometry": {1}{4}}}{5}'.format(attributes_str, geometry_str, NL, NL, NL, NL)
            else:
                row_json_str = u'{{{1}"attributes": {0}{2}}}{3}'.format(attributes_str, NL, NL, NL)

            ftmp.write(row_json_str)

##################################################
class JUError(Exception):
    reason = ''
    def __init__(self, reason):
        exep_info = None
        for ei in sys.exc_info() :
            if isinstance(ei, Exception) :
                exep_info = str(ei)
  
        self.reason = reason + ('. ' + exep_info) if exep_info is not None else ""
    def __str__(self):
        return self.reason
