## GIS2BIM within FreeCAD

import GIS2BIM
import Draft
import Part
import FreeCAD
import Arch

SiteName = "GIS2BIM-Sitedata"
TempFolderName = "GIStemp/"

def CreateTempFolder(Name):
	FileName = FreeCAD.ActiveDocument.FileName
		if FreeCAD.ActiveDocument.FileName is ""
#			"Melding please save file first
	NewFolder = str.split(FileName,str.split(FileName,"/")[-1])[0] + Name
	#if new folder exist then skip other
	return NewFolder

def ImportImage(fileLocation,width,height,scale,name):
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
	SiteObject.Longitude = Longitude
	SiteObject.Latitude = Latitude
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

def ArchSiteAddparameters(SiteObject):
	SiteObject.addProperty("App::PropertyString","CRS_EPSG_SRID")
	SiteObject.addProperty("App::PropertyString","CRS_EPSG_Description")
	SiteObject.addProperty("App::PropertyFloat","CRS_x")
	SiteObject.addProperty("App::PropertyFloat","CRS_y")
	SiteObject.addProperty("App::PropertyFloat","BoundingboxWidth")
	SiteObject.addProperty("App::PropertyFloat","BoundingboxHeight")
	SiteObject.CRS_EPSG_SRID = "28992"
	SiteObject.CRS_EPSG_Description = "RD-coordinaten"
	SiteObject.CRS_x = 104500
	SiteObject.CRS_y = 450000
	SiteObject.BoundingboxWidth = 500
	SiteObject.BoundingboxHeight = 500
	SiteObject.Orientation = u"True North"