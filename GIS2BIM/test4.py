import GIS2BIM_FreeCAD
import GIS2BIM
import GIS2BIM_NL
import importlib
importlib.reload(GIS2BIM_FreeCAD)

import FreeCAD

SiteName = "GIS-Sitedata"
TempFolderName = "GIStemp/"

sitename = SiteName

#Get/set parameters for GIS
tempFolderName = "GIStemp/"
X = GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_x
Y = GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_y
lat = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).WGS84_Latitude)
lon = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).WGS84_Longitude)
bboxWidthStart = GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).BoundingboxWidth
bboxHeightStart = GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).BoundingboxHeight
CRS = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_EPSG_SRID)
CRSDescription = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_EPSG_Description)
bboxString = GIS2BIM.CreateBoundingBox(GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_x,GIS2BIM_FreeCAD.ArchSiteCreateCheck(sitename).CRS_y,bboxWidthStart,bboxHeightStart,0)

GIS_2D_Ruimtelijke_Plannen = GIS2BIM_FreeCAD.CreateLayer("GIS_2D_Ruimtelijke_Plannen")	
test = RuimtelijkePlannenBouwvlakCurves = GIS2BIM_FreeCAD.CurvesFromWFS(GIS2BIM_NL.NLRuimtelijkeplannenBouwvlak,bboxString,".//{http://www.opengis.net/gml}posList",-X,-Y,1000,3,False, False,u"Solid",(0.0,0.0,1.0))

print(test)