#BAG 3D V2 

import importlib
import GIS2BIM
import GIS2BIM_NL
import GIS2BIM_FreeCAD
import GIS2BIM_CRS 
import GIS2BIM_GUI
importlib.reload(GIS2BIM_NL)
importlib.reload(GIS2BIM_FreeCAD)

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

jsonFileNames = GIS2BIM_NL.BAG3DDownload(bboxString,tempFolder)
	
#Import JSON
for jsonFile in jsonFileNames:
	GIS2BIM_FreeCAD.CityJSONImport(jsonFile,X,Y,2,bboxWidthStart,bboxHeightStart)

FreeCAD.ActiveDocument.recompute()
