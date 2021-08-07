## GIS2BIM within FreeCAD

import GIS2BIM
import Draft
import Part
import FreeCAD
import Arch
import os
from PySide2 import QtCore, QtWidgets, QtGui

SiteName = "GIS2BIM-Sitedata"
TempFolderName = "GIStemp/"

def CreateTempFolder(Name):
#Create a temporary subfolder in the folder of the projectfile to store temporary GIS-files
	FileName = FreeCAD.ActiveDocument.FileName
	if len(str(FreeCAD.ActiveDocument.FileName)) < 1:
		dialog = QtWidgets.QMessageBox()
		dialog.setText("Please save your project so that FreeCAD-GIS can create a temporary folder for GIS-files")
		dialog.setWindowTitle("Warning")
		dialog.exec_() 
	else:
		NewFolder = os.path.dirname(FileName) + "/" + Name
		if os.path.exists(NewFolder):
			NewFolder
		else:
			os.mkdir(NewFolder)
	return NewFolder

def ImportImage(fileLocation,width,height,scale,name):
#Import image in view
    Img = FreeCAD.activeDocument().addObject('Image::ImagePlane',name)
    Img.ImageFile = fileLocation
    Img.XSize = width*scale
    Img.YSize = height*scale
    Img.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0.000000,0.000000,0.000000,1.000000))
    return Img

def Buildings3D(curves3DBAG,heightData3DBAG):
    solids = []
    for i,j,k in zip(curves3DBAG,heightData3DBAG[1],heightData3DBAG[2]):
        pointlist = []
        for curve in i:
            pointlist.append(FreeCAD.Vector(curve[0], curve[1], float(j)*1000))
        a = Part.makePolygon(pointlist)
        face = Part.Face(a)
        solid = face.extrude(FreeCAD.Vector(0, 0, float(k) * 1000))
        sld = Part.show(solid)
        solids.append(sld)
    return solids

def CurvesFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions,closedValue,DrawStyle,LineColor):
    curves = GIS2BIM.PointsFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    curvesWFS = []
    for i in curves:
        pointlist = []
        for j in i:
            pointlist.append(FreeCAD.Vector(j[0], j[1], 0))
        a = Draft.makeWire(pointlist, closed=closedValue)
        a.MakeFace = closedValue
        a.ViewObject.DrawStyle = DrawStyle
        a.ViewObject.LineColor = LineColor
        curvesWFS.append(a)
    return curvesWFS

def PlaceText(textData,fontSize, upper):
    Texts = []
    for i, j, k in zip(textData[0], textData[1], textData[2]):
        ZAxis = FreeCAD.Vector(0, 0, 1)
        p1 = FreeCAD.Vector(i[0][0], i[0][1], 0)
        Place1 = FreeCAD.Placement(p1, FreeCAD.Rotation(ZAxis, -float(j)))
        if upper:
           k = k.upper()
        else: k = k
        Text1 = Draft.makeText(k, point=p1)
        Text1.ViewObject.FontSize = fontSize
        Text1.Placement = Place1
        Texts.append(Text1)
    return Texts

def ArchSiteCreateCheck(SiteName):
#Create an ArchSiteobject which is used to store data nessecary for GIS2BIM. 
	lstObjects = []
	for obj in FreeCAD.ActiveDocument.Objects: #Check is SiteObject already exists and fill parameters
	    lstObjects.append(obj.Label)
	if SiteName in lstObjects: 
		ArchSiteObject = FreeCAD.ActiveDocument.Objects[lstObjects.index(SiteName)]
	else: #Create Siteobject and add parameters
	    ArchSiteObject = Arch.makeSite([],[],SiteName)
	    ArchSiteAddparameters(ArchSiteObject)
		
	return ArchSiteObject

def ArchSiteFilldata(SiteObject,Longitude,Latitude,TrueNorth,Address,Country,City,PostalCode,CRS_EPSG_SRID,CRS_EPSG_Description,CRS_x,CRS_y,BoundingboxWidth,BoundingboxHeight):
	#buildin
	SiteObject.WGS84_Longitude = Longitude
	SiteObject.WGS84_Latitude = Latitude
	SiteObject.Orientation = u"True North"
	SiteObject.Address = Address
	SiteObject.Country = Country
	SiteObject.City = City
	SiteObject.PostalCode = ""
	SiteObject.CRS_EPSG_SRID = CRS_EPSG_SRID
	SiteObject.CRS_EPSG_Description = CRS_EPSG_Description
	SiteObject.CRS_x = CRS_x
	SiteObject.CRS_y = CRS_y
	SiteObject.BoundingboxWidth = BoundingboxWidth
	SiteObject.BoundingboxHeight = BoundingboxHeight
	return SiteObject

def ArchSiteAddparameters(SiteObject):
	SiteObject.addProperty("App::PropertyString","CRS_EPSG_SRID")
	SiteObject.addProperty("App::PropertyString","CRS_EPSG_Description")
	SiteObject.addProperty("App::PropertyString","WGS84_Longitude")
	SiteObject.addProperty("App::PropertyString","WGS84_Latitude")
	SiteObject.addProperty("App::PropertyFloat","CRS_x")
	SiteObject.addProperty("App::PropertyFloat","CRS_y")
	SiteObject.addProperty("App::PropertyFloat","BoundingboxWidth")
	SiteObject.addProperty("App::PropertyFloat","BoundingboxHeight")
	SiteObject.WGS84_Longitude = "4.659201"
	SiteObject.WGS84_Latitude = "51.814213"
	SiteObject.BoundingboxWidth = 500
	SiteObject.BoundingboxHeight = 500	
	return SiteObject