import GIS2BIM
import GIS2BIM_FreeCAD
import importlib
import json
importlib.reload(GIS2BIM_FreeCAD)

#jsonfile = "C:/TEMP/GIStemp/BAG3D/3dbag_v21031_7425c21b_2981.json"
jsonFile = "C:/TEMP/DenHaag_01.json"

#GIS2BIM_FreeCAD.CityJSONImport(jsonfile, "80661", "455018",2)
#GIS2BIM_FreeCAD.CityJSONImport(jsonfile, "78248", "457604",0)
dX = "78248"
dY = "457604"
LODnumber = 0

#Import CityJSON File, jsonfilename, dx and dy in string/meters
layer = GIS2BIM_FreeCAD.CreateLayer("CityJSON")	
data = json.load(open(jsonFile,))
vert = data['vertices']
cityobj = data['CityObjects']
translate = data['transform']['translate']
scaleX = data['transform']['scale'][0]
scaleY = data['transform']['scale'][1]
scaleZ = data['transform']['scale'][2]
translatex = (translate[0] -float(dX))/scaleX
translatey = (translate[1] -float(dY))/scaleY
translatez = -translate[2]/scaleZ

#for j in data['CityObjects'][objName]['geometry'][LODnumber]['boundaries']:	

meshes = []
for i in cityobj:
	objName = i
	data2 = data['CityObjects'][objName]['geometry'].values()
	#data3 = len(data2)
		#for k in j:		
	meshes.append(data2)	
		#facets = []
		##	facets.append(((vert[k[0][0]][0]+translatex, vert[k[0][0]][1]+translatey, vert[k[0][0]][2]+translatez),(vert[k[0][1]][0]+translatex, vert[k[0][1]][1]+translatey, vert[k[0][1]][2]+translatez),(vert[k[0][2]][0]+translatex, vert[k[0][2]][1]+translatey, vert[k[0][2]][2]+translatez)))
		#m = Mesh.Mesh(facets)
		#f = FreeCAD.activeDocument().addObject("Mesh::Feature", objName)
		#f.Mesh = m
		#meshes.append(f.Mesh)
		#FreeCAD.activeDocument().getObject("CityJSON").addObject(f)
print(meshes, data3)