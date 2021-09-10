#BGT IMPORTER

xpath1 = './/{http://www.opengis.net/gml}featureMember'
xpath2 = './/{http://www.opengis.net/gml}pos'
xpath3 = './/{http://www.geostandaarden.nl/imgeo/2.1/simple/gml31}openbareRuimteNaam.tekst'
xpath4 = './/{http://www.geostandaarden.nl/imgeo/2.1/simple/gml31}openbareRuimteNaam.positie_1.hoek'

import GIS2BIM
import GIS2BIM_NL
import GIS2BIM_FreeCAD

import xml.etree.ElementTree as ET
import importlib
importlib.reload(GIS2BIM)
importlib.reload(GIS2BIM_NL)
importlib.reload(GIS2BIM_FreeCAD)

sitename = "GIS-Sitedata"
tempFolderName = "GIStemp/"

X = GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_x
Y = GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_y
bboxWidth = GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).BoundingboxWidth
bboxHeight = GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).BoundingboxHeight
timeout = 150
folderBGT = GIS2BIM_FreeCAD.CreateTempFolder(tempFolderName+ '/BGT')	
filepathZIP = folderBGT + '.zip'

#Download BGT
URL = GIS2BIM_NL.bgtDownloadURL(X,Y,bboxWidth,bboxHeight,timeout)
GIS2BIM.downloadUnzip(URL,filepathZIP,folderBGT)

#Create Curves

bgt_curves_faces = ["bgt_begroeidterreindeel",
"bgt_onbegroeidterreindeel",
"bgt_ondersteunendwaterdeel",
"bgt_ondersteunendwegdeel",
"bgt_overbruggingsdeel",
"bgt_overigbouwwerk",
"bgt_pand",
"bgt_waterdeel",
"bgt_wegdeel"]

bgt_curves_faces_color = [(223/255,230/255,208/255),
(223/255,230/255,208/255),
(205/255,230/255,237/255),
(226/255,226/255,226/255),
(234/255,234/255,234/255),
(220/255,155/255,140/255),
(220/255,155/255,140/255),
(205/255,230/255,237/255),
(234/255,234/255,234/255)]

bgt_curves_lines = ["bgt_functioneelgebied",
"bgt_gebouwinstallatie",
"bgt_kunstwerkdeel",
"bgt_overbruggingsdeel",
"bgt_overigbouwwerk",
"bgt_overigescheiding",
"bgt_scheiding",
"bgt_spoor",
"bgt_tunneldeel"]

xpath = './/{http://www.opengis.net/gml}posList'

GIS2BIM_FreeCAD.CreateLayer("BGT")

#Draw bgt_curves_lines
for i in bgt_curves_lines:
	path = folderBGT + '/' + i + '.gml'
	tree = ET.parse(path)
	Curves = GIS2BIM_FreeCAD.CurvesFromGML(tree,xpath,-X,-Y,bboxWidth,bboxHeight,1000,0,0,0,"Solid",(0.7,0.0,0.0),(0.0,0.0,0.0))
	GIS2BIM_FreeCAD.CreateLayer(i)
	FreeCAD.activeDocument().getObject(i).addObjects(Curves)
	FreeCAD.activeDocument().getObject("BGT").addObject(FreeCAD.activeDocument().getObject(i))
	FreeCAD.ActiveDocument.recompute()

for i,j in zip(bgt_curves_faces,bgt_curves_faces_color):
	path = folderBGT + '/' + i + '.gml'
	tree = ET.parse(path)
	Curves = GIS2BIM_FreeCAD.CurvesFromGML(tree,xpath,-X,-Y,bboxWidth,bboxHeight,1000,2,1,1,"Solid",(0.7,0.0,0.0),j)
	GIS2BIM_FreeCAD.CreateLayer(i)
	FreeCAD.activeDocument().getObject(i).addObjects(Curves)
	FreeCAD.activeDocument().getObject("BGT").addObject(FreeCAD.activeDocument().getObject(i))
	FreeCAD.ActiveDocument.recompute()
