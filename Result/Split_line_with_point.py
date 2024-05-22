
# Define the path of the layers 
point_layer_path = r"C:\Users\jjtakodjou\Desktop\GitHub\Tasks_Automation\Data\point.shp"
line_layer_path = r"C:\Users\jjtakodjou\Desktop\GitHub\Tasks_Automation\Data\Line.shp"

# Create vector layer
point_layer = QgsVectorLayer(point_layer_path, 'Point', 'ogr')
line_layer = QgsVectorLayer(line_layer_path, 'Line', 'ogr')

# Add layer to the currect project 
if not point_layer.isValid() or  not line_layer.isValid():
    print("Layer failed to load !")
else:
    QgsProject.instance().addMapLayer(point_layer)
    QgsProject.instance().addMapLayer(line_layer)
    
# Snap point to line 
results = processing.run("native:snapgeometries", {'INPUT':point_layer_path,
'REFERENCE_LAYER':line_layer_path,'TOLERANCE':10,'BEHAVIOR':3,
'OUTPUT':'TEMPORARY_OUTPUT'})

snapped_point = results['OUTPUT']

# Create buffer from the snapped point
results = processing.run("native:buffer", {'INPUT': snapped_point,
'DISTANCE':0.00001,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,
'OUTPUT':'TEMPORARY_OUTPUT'})
buffer_snap_point = results['OUTPUT']

# Convert buffer (polygon) to line
results = processing.run("native:polygonstolines", {'INPUT':buffer_snap_point,
'OUTPUT':'TEMPORARY_OUTPUT'})
line_from_snap_point = results['OUTPUT']
 
# Split line and load the result 
results = processing.runAndLoadResults("native:splitwithlines", {'INPUT': line_layer_path,
 'LINES':line_from_snap_point,
 'OUTPUT':'Split_Lines'})
