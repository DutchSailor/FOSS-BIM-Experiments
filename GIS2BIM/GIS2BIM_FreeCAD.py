## GIS2BIM within FreeCAD

import GIS2BIM
import Draft
import Part
import FreeCAD

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