#BAG 3D V2 

import importlib
import GIS2BIM
import GIS2BIM_FreeCAD
import GIS2BIM_CRS 
import GIS2BIM_GUI
importlib.reload(GIS2BIM)

import Mesh

import urllib
import urllib.request
import requests

import xml.etree.ElementTree as ET
import json

sitename = "GIS-Sitedata"

tempFolderName = "GIStemp/BAG3D/"
tempFolder = GIS2BIM_FreeCAD.CreateTempFolder(tempFolderName)

X = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_x)
Y = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_y)	
dx = -float(X) * 1000
dy = -float(Y) * 1000

bboxWidthStart = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).BoundingboxWidth)
bboxHeightStart = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).BoundingboxHeight)

bboxString = GIS2BIM.CreateBoundingBox(float(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_x),float(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_y),float(bboxWidthStart),float(bboxHeightStart),0)

url = "https://data.3dbag.nl/api/BAG3D_v2/wfs?&request=GetFeature&typeName=BAG3D_v2:bag_tiles_3k&bbox="
xPathString1 = ".//{bag3d_v2}tile_id"
xPathString2 = ".//{http://www.opengis.net/gml/3.2}posList"
xPathString3 = ".//{bag3d_v2}bag_tiles_3k"

#Webrequest to obtain tilenumbers based on bbox
urlreq = url + bboxString
urlFile = urllib.request.urlopen(urlreq)
tree = ET.parse(urlFile)

urlDownloadPrefix = "http://data.3dbag.nl/cityjson/v21031_7425c21b/3dbag_v21031_7425c21b_"

#Collect result of webrequest is correct format
res = []
for i,j,k in zip(tree.findall(xPathString1),tree.findall(xPathString2),tree.findall(xPathString3)):
	LBcoords = j.text.split()[2], j.text.split()[3]
	res.append((i.text, LBcoords, k.text, urlDownloadPrefix + i.text + ".json"))

#Download files
jsonFileNames = []
for i in res:
	fileNme = tempFolder + '3dbag_v21031_7425c21b_' + i[0]+ '.json' 	
	r = requests.get(i[3])
	open(fileNme, 'wb').write(r.content)	
	jsonFileNames.append(fileNme)

#Import JSON
for jsonFile in jsonFileNames:
	layer = GIS2BIM_FreeCAD.CreateLayer("CityJSON")	
	data = json.load(open(jsonFile,))
	vert = data['vertices']
	cityobj = data['CityObjects']
	translate = data['transform']['translate']
	translatex = (translate[0] -float(X))*1000
	translatey = (translate[1] -float(Y))*1000
	translatez = -translate[2]*1000

	for i in cityobj:
		objName = i
		for j in data['CityObjects'][objName]['geometry'][2]['boundaries']:	
			facets = []
			for k in j:
				facets.append(((vert[k[0][0]][0]+translatex, vert[k[0][0]][1]+translatey, vert[k[0][0]][2]+translatez),(vert[k[0][1]][0]+translatex, vert[k[0][1]][1]+translatey, vert[k[0][1]][2]+translatez),(vert[k[0][2]][0]+translatex, vert[k[0][2]][1]+translatey, vert[k[0][2]][2]+translatez)))
			m = Mesh.Mesh(facets)
			f = FreeCAD.activeDocument().addObject("Mesh::Feature", objName)
			f.addProperty("App::PropertyString","fid") 
			f.addProperty("App::PropertyString","identificatie") 
			f.addProperty("App::PropertyString","oorspronkelijk_bouwjaar") 
			f.addProperty("App::PropertyString","status") 
			f.Mesh = m
			#f.Placement = FreeCAD.Placement(FreeCAD.Vector(translatex,translatey,translatez),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
			FreeCAD.activeDocument().getObject("CityJSON").addObject(f)

FreeCAD.ActiveDocument.recompute()
