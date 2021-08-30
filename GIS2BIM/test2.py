import GIS2BIM
import GIS2BIM_FreeCAD
import importlib
importlib.reload(GIS2BIM)
importlib.reload(GIS2BIM_FreeCAD)
import xml.etree.ElementTree as ET

bgtfolder = 'C:/Users/mikev/OneDrive/Bureaublad/TEMP/GIStemp/BGT'

bgt_curves = ["bgt_begroeidterreindeel",
"bgt_functioneelgebied",
"bgt_gebouwinstallatie",
"bgt_kunstwerkdeel",
"bgt_onbegroeidterreindeel",
"bgt_ondersteunendwaterdeel",
"bgt_ondersteunendwegdeel",
"bgt_overbruggingsdeel",
"bgt_overigbouwwerk",
"bgt_overigescheiding",
"bgt_pand",
"bgt_scheiding",
"bgt_spoor",
"bgt_tunneldeel",
"bgt_waterdeel",
"bgt_wegdeel"]

xpath = './/{http://www.opengis.net/gml}posList'
x = 122276.780
y = 486273.120
b = 300
h = 300

file_paths = []
for i in bgt_curves:
	path = bgtfolder + '/' + i + '.gml'
	tree = ET.parse(path)
	Curves = GIS2BIM_FreeCAD.CurvesFromGML(tree,xpath,-x,-y,b,h,1000,2,0,0,"Solid",(0.7,0.0,0.0))
	GIS2BIM_FreeCAD.CreateLayer(i)
	FreeCAD.activeDocument().getObject(i).addObjects(Curves)
	FreeCAD.ActiveDocument.recompute()

#GIS2BIM_FreeCAD.CurvesFromGML(file_paths[11], './/{http://www.opengis.net/gml}posList', -122276.780, -486273.120, 1000, 2, 0, 0,"Solid",(0.7,0.0,0.0))
#test = GIS2BIM.filterGMLbbox(tree,xpath,122276.780,486273.120,500,500,1000)
#test2 = GIS2BIM.GML_poslistData(tree, xpath,-122276.780,-486273.120,1000,2)


#print(test2)
