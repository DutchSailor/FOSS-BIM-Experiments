XPATH STRINGS
.//{http://www.opengis.net/gml}pos
.//{http://www.geostandaarden.nl/imgeo/2.1/simple/gml31}plus-type
.//{http://www.opengis.net/gml}featureMember
.//{http://www.opengis.net/gml}pos
.//{http://www.geostandaarden.nl/imgeo/2.1/simple/gml31}openbareRuimteNaam.tekst
.//{http://www.geostandaarden.nl/imgeo/2.1/simple/gml31}openbareRuimteNaam.positie_1.hoek


BGT DOWNLOAD
import sys
import clr
import json
import urllib
import time

polygonString = IN[0] #Define format, polygon, layers
url = IN[1]
url2= IN[2]
timeout = IN[3]
folder = IN[4]
folder2 = IN[5]
pathRequestsLibrary = IN[6]

sys.path.append(pathRequestsLibrary)
import requests
from requests.structures import CaseInsensitiveDict

##Define data 
qryPart1 = '{"featuretypes":['
qryPart2 = '"bak","begroeidterreindeel","bord","buurt","functioneelgebied","gebouwinstallatie","installatie","kast","kunstwerkdeel","mast","onbegroeidterreindeel","ondersteunendwaterdeel","ondersteunendwegdeel","ongeclassificeerdobject","openbareruimte","openbareruimtelabel","overbruggingsdeel","overigbouwwerk","overigescheiding","paal","pand","put","scheiding","sensor","spoor","stadsdeel","straatmeubilair","tunneldeel","vegetatieobject","waterdeel","waterinrichtingselement","waterschap","weginrichtingselement","wijk","wegdeel"'
qryPart3 = '],"format":"gmllight","geofilter":"POLYGON('
qryPart4 = polygonString
qryPart5 = ')"}'

data = qryPart1 +  qryPart2 + qryPart3 + qryPart4 + qryPart5
dataquery = data

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["Content-Type"] = "application/json"

resp = requests.post(url, headers=headers, data=data)

jsondata = json.loads(resp.text)
data = jsondata["downloadRequestId"]
urlstatus = url + "/" + data + "/status" 

# Check URL Status

req = urllib.request.urlopen(urlstatus)
req2 = req.read().decode('utf-8')
progressStatus = int(json.loads(req2)['progress'])

timer = 0

while timer < timeout:
    req = urllib.request.urlopen(urlstatus)
    req2 = req.read().decode('utf-8')    
    progressStatus = int(json.loads(req2)['progress'])
    status = json.loads(req2)['status']
    if status == "COMPLETED":
        try:
            downloadURL = url2 + json.loads(req2)["_links"]["download"]["href"]
        except:   
            downloadURL = "unable to get downloadlink"        
        message = status
        break
    elif timer > timeout:
        downloadURL = "empty"
        message = "timeout"
        break
    else: 
        time.sleep(1)
    timer = timer + 1

#downloadURL = "test"
#message = "test"
req = requests.get(downloadURL, allow_redirects=True)

with open(folder, 'wb') as f:
    f.write(req.content)

OUT = downloadURL, message, urlstatus, folder, folder2, dataquery



BGT GEOMETRY CURVES

import sys
sys.path.append("C:\Program Files (x86)\IronPython 2.7\Lib")

import clr
import re
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import xml.etree.ElementTree as ET
aDebug = []

directory_path = IN[0]

bgt_curves = ["bgt_begroeidterreindeel",
"bgt_functioneelgebied",
"bgt_gebouwinstallatie",
"bgt_kunstwerkdeel",
"bgt_onbegroeidterreindeel",
"bgt_ondersteunendwaterdeel",
"bgt_ondersteunendwegdeel",
"bgt_ongeclassifiseerdobject",
"bgt_overbruggingsdeel",
"bgt_overigbouwwerk",
"bgt_overigescheiding",
"bgt_pand",
"bgt_scheiding",
"bgt_spoor",
"bgt_tunneldeel",
"bgt_waterdeel",
"bgt_wegdeel"]

file_paths = []
for i in bgt_curves:
	file_paths.append(directory_path + '/' + i + '.gml')

def checkIfCoordIsInsideBoundingBox(coord, min_x, min_y, max_x, max_y):
	if re.match(r'^-?\d+(?:\.\d+)$', coord[0]) is None or re.match(r'^-?\d+(?:\.\d+)$', coord[1]) is None:
		return False
	else:
		if min_x <= float(coord[0]) <= max_x and min_y <= float(coord[1]) <= max_y:
			return True
		else:
		    return False
	
def mainFunction(file_path):
    # Inputs
	
    xpathstr = IN[1]

    # Bounding box definition
    bbx = IN[2]
    bby = IN[3]
    bb_size = IN[4]
    scale = IN[5]
    bounding_box = [bbx, bby, bb_size]
    min_x = bounding_box[0] - (bounding_box[2]/2)#/2
    min_y = bounding_box[1] - (bounding_box[2]/2)
    max_x = bounding_box[0] + (bounding_box[2]/2)
    max_y = bounding_box[1] + (bounding_box[2]/2)

    # get data from xml
    tree = ET.parse(file_path)
    root = tree.getroot()

    # for loop to get each element in an array
    XMLelements = []
    for elem in root.iter():
        XMLelements.append(elem)

    xpathfound = root.findall(xpathstr)

    # for loop to get all polygons in an array
    polygons = []
    for x in xpathfound:
        if x.text:
            try:
                polygons.append(x.text)
            except:
                polygons.append("_none_")
        else:
            polygons.append("_none_")

    # for loop to get each polygon as a list instead of a string
    newPolygons = []
    for polygon in polygons:
        newPolygons.append(polygon.split(" "))

    # for loop to get x,y coords and filter polygons inside Bounding Box
    xyPolygons = []
    for newPolygon in newPolygons:
        polygon_is_inside_bounding_box = False
        x = 0
        xyPolygon = []
        for i in range(0, int(len(newPolygon) / 2)):
            xy_coord = [newPolygon[x], newPolygon[x + 1]]
            xy_coord_trans = [round((float(newPolygon[x])-bbx)*scale), round((float(newPolygon[x + 1])-bby)*scale)]
            xyPolygon.append(xy_coord_trans)
            x += 2
            if checkIfCoordIsInsideBoundingBox(xy_coord, min_x, min_y, max_x, max_y):
                polygon_is_inside_bounding_box = True
        if polygon_is_inside_bounding_box:
            xyPolygons.append(xyPolygon)
    return xyPolygons

# execution of main function in python script
returnValue = []
for i in file_paths:
	try:
		returnValue.append(mainFunction(i))
	except:
		returnValue.append("_none_")
		
# put returnValue in OUT
OUT = returnValue


BGT POINTS METADATA

import sys
sys.path.append("C:\Program Files (x86)\IronPython 2.7\Lib")

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import xml.etree.ElementTree as ET

directory_path = IN[0]

bgt_points = ["bgt_bak",
"bgt_bord",
"bgt_kast",
"bgt_mast",
"bgt_paal",
"bgt_put",
"bgt_sensor",
"bgt_straatmeubilair",
"bgt_vegetatieobject",
"bgt_waterinrichtingselement",
"bgt_wegrichtingselement"]

file_paths = []
for i in bgt_points:
	file_paths.append(directory_path + '/' + i + '.gml')
	
def checkIfCoordIsInsideBoundingBox(coord, bounding_box):
    min_x = bounding_box[0] - (bounding_box[2] / 2)
    min_y = bounding_box[1] - (bounding_box[2] / 2)
    max_x = bounding_box[0] + (bounding_box[2] / 2)
    max_y = bounding_box[1] + (bounding_box[2] / 2)

    if min_x <= float(coord[0]) <= max_x and min_y <= float(coord[1]) <= max_y:
        return True
    else:
        return False

def mainFunction(file_path):
    # Inputs
    xpathstr = IN[1]
    # Bounding box definition
    bbx = IN[2]
    bby = IN[3]
    bb_size = IN[4]
    xpathstr2 = IN[5]
    scale = IN[6]
    bounding_box = [bbx, bby, bb_size]
    # get data from xml
    tree = ET.parse(file_path)
    root = tree.getroot()
	
    # for loop to get each element in an array
    XMLelements = []
    for elem in root.iter():
        XMLelements.append(elem)

    xpathfound = root.findall(xpathstr)
    xpathfoundlabel = root.findall(xpathstr2)
    # for loop to get all points in an array
    points = []
    for x in xpathfound:
        if x.text:
            try:
                points.append(x.text)
            except:
                points.append("_none_")
        else:
            points.append("_none_")
	
	labels = []
    for i in xpathfoundlabel:
        if i.text:
            try:
                labels.append(i.text)
            except:
                labels.append("_none_")
        else:
            labels.append("_none_")
    
    # for loop to get each point as a list instead of a string
    newPoints = []
    newPointsTrans = []
    for point in points:
    	newPointsTrans.append([round((float((point.split(" ")[0]))-bbx)*scale),round((float((point.split(" ")[1]))-bby)*scale)])
        newPoints.append(point.split(" "))

    # for loop to get x,y coords and filter points inside Bounding Box
    xyPoints = []
    xyLabels = []
    for newPoint,newPointTrans, label in zip(newPoints, newPointsTrans, labels):
    	point_is_inside_bounding_box = False
    	if checkIfCoordIsInsideBoundingBox(newPoint, bounding_box):
    		point_is_inside_bounding_box = True
    		xyPoints.append(newPointTrans)
    		xyLabels.append(label)
    return xyPoints, xyLabels

# execution of main function in python script
returnValue = []
for i in file_paths:
	try:
		returnValue.append(mainFunction(i))
	except:
		returnValue.append("_none_")

# put returnValue in OUT
OUT = returnValue, bgt_points

BGT LABELS

import sys
sys.path.append("C:\Program Files (x86)\IronPython 2.7\Lib")

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import xml.etree.ElementTree as ET


def checkIfCoordIsInsideBoundingBox(coord, bounding_box):
    min_x = bounding_box[0] - (bounding_box[2] / 2)
    min_y = bounding_box[1] - (bounding_box[2] / 2)
    max_x = bounding_box[0] + (bounding_box[2] / 2)
    max_y = bounding_box[1] + (bounding_box[2] / 2)

    if min_x <= float(coord[0]) <= max_x and min_y <= float(coord[1]) <= max_y:
        return True
    else:
        return False

def mainFunction():
    # Inputs
    file_path = IN[0]
    xpathstr = IN[1]
    # Bounding box definition
    bbx = IN[2]
    bby = IN[3]
    bb_size = IN[4]
    xpathstr2 = IN[5]
    xpathstr3 = IN[6]
    xpathstr4 = IN[7]
    scale = IN[8]
    bounding_box = [bbx, bby, bb_size]
    # get data from xml
    tree = ET.parse(file_path)
    root = tree.getroot()
	
    # for loop to get each element in an array
    XMLelements = []
    for elem in root.iter():
        XMLelements.append(elem)

    xpathfound = root.findall(xpathstr)
    xpathfoundlabel = root.findall(xpathstr3)
    xpathfoundrotation = root.findall(xpathstr4)
    
    xpathpoints = []
    for i in xpathfound:
    	xpathpoints.append(i.findall(xpathstr2))
    	
    points = []
    for y in xpathpoints:
    	subpoints = []
    	for x in y:
        	if x.text:
        	    try:
        	        subpoints.append(x.text)
        	    except:
        	        subpoints.append("_none_")
        	else:
        	    subpoints.append("_none_")
        points.append(subpoints[0])	    
    # for loop to get all points in an array

	labels = []
    for i in xpathfoundlabel:
        if i.text:
            try:
                labels.append(i.text)
            except:
                labels.append("_none_")
        else:
            labels.append("_none_")
        
    rotations = []
    for i in xpathfoundrotation:
        if i.text:
            try:
                rotations.append(i.text)
            except:
                rotations.append("_none_")
        else:
            rotations.append("_none_")
    
    # for loop to get each point as a list instead of a string
    newPoints = []
    newPointsTrans = []
    for point in points:
    	newPointsTrans.append([round((float((point.split(" ")[0]))-bbx)*scale),round((float((point.split(" ")[1]))-bby)*scale)])
        newPoints.append(point.split(" "))

    # for loop to get x,y coords and filter points inside Bounding Box
    xyPoints = []
    xyLabels = []
    xyRotations = []
    for newPoint, newPointTrans, label, rotation in zip(newPoints, newPointsTrans, labels, rotations):
    	point_is_inside_bounding_box = False
    	if checkIfCoordIsInsideBoundingBox(newPoint, bounding_box):
    		point_is_inside_bounding_box = True
    		xyPoints.append(newPointTrans)
    		xyLabels.append(label)
    		xyRotations.append(rotation)
    return xyPoints, xyLabels, xyRotations, points

# execution of main function in python script
returnvalue = mainFunction()

# put returnValue in OUT
OUT = returnvalue