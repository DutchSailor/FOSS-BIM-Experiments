## snapGIS Library

## snapGIS within FreeCAD

#import snapGIS_Lib
import urllib.request
import urllib
import xml.etree.ElementTree as ET
import json
import Draft
import Part

def snapGIS_FreeCAD_ImportImage(fileLocation,width,height,scale):
    App.activeDocument().addObject('Image::ImagePlane','ImagePlane')
    App.activeDocument().ImagePlane.ImageFile = fileLocation
    App.activeDocument().ImagePlane.XSize = width*scale
    App.activeDocument().ImagePlane.YSize = height*scale
    App.activeDocument().ImagePlane.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))

def snapGIS_FreeCAD_3DBuildings(curves3DBAG,heightData3DBAG):
    for i,j,k in zip(curves3DBAG,heightData3DBAG[1],heightData3DBAG[2]):
        pointlist = []
        for curve in i:
            pointlist.append(FreeCAD.Vector(curve[0], curve[1], float(j)*1000))
        a = Part.makePolygon(pointlist)
        face = Part.Face(a)
        solid = face.extrude(FreeCAD.Vector(0, 0, float(k) * 1000))
        Part.show(solid)
    return solid

def snapGIS_FreeCAD_CurvesFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions,closedValue,DrawStyle,LineColor):
    curves = snapGIS_PointsFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    for i in curves:
        pointlist = []
        for j in i:
            pointlist.append(FreeCAD.Vector(j[0], j[1], 0))
        a = Draft.makeWire(pointlist, closed=closedValue)
        a.MakeFace = closedValue
        a.ViewObject.DrawStyle = DrawStyle
        a.ViewObject.LineColor = LineColor
    return a

def snapGIS_FreeCAD_PlaceText(textData,fontSize):
    for i, j, k in zip(textData[0], textData[1], textData[2]):
        ZAxis = FreeCAD.Vector(0, 0, 1)
        p1 = FreeCAD.Vector(i[0][0], i[0][1], 0)
        Place1 = FreeCAD.Placement(p1, FreeCAD.Rotation(ZAxis, -float(j)))
        Text1 = Draft.makeText(k, point=p1)
        Text1.ViewObject.FontSize = fontSize
        Text1.Placement = Place1
    return Text1
