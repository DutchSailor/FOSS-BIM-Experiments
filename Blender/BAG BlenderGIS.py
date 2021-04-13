## GIS2BIM Library

## Webserverdata
DutchGEO_PDOKServerURL = "http://geodata.nationaalgeoregister.nl/locatieserver/v3/free?wt=json&rows=1&q="

DutchGEOCadastreServerRequest1 = "http://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0?service=WFS&version=2.0.0&request=GetFeature&typeName=perceel&bbox="
#For curves of Cadastral Parcels

DutchGEOCadastreServerRequest2 = "http://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0?service=WFS&version=2.0.0&request=GetFeature&typeName=kadastralekaartv4:nummeraanduidingreeks&bbox="
#For 'nummeraanduidingreeks' of Cadastral Parcels

DutchGEOCadastreServerRequest3 = "http://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0?service=WFS&version=2.0.0&request=GetFeature&typeName=kadastralekaartv4:openbareruimtenaam&bbox="
#For 'openbareruimtenaam' of Cadastral Parcels

DutchGEOBAG = "http://geodata.nationaalgeoregister.nl/bag/wfs/v1_1?service=wfs&version=2.0.0&request=GetFeature&typeName=bag:pand&bbox="
#Building Contour of BAG

DutchGEOBAG3D = "http://3dbag.bk.tudelft.nl/data/wfs?&request=GetFeature&typeName=BAG3D:pand3d&outputFormat=GML3&bbox="
#3D Buildings of BAG

DutchGEOLuchtfoto2019WMS = "http://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?&request=GetMap&VERSION=1.3.0&STYLES=&layers=2019_ortho25&width=3000&height=3000&format=image/png&crs=EPSG:28992&bbox="

DutchGEORuimtelijkeplannenBouwvlakServerRequest = "http://afnemers.ruimtelijkeplannen.nl/afnemers/services?&service=WFS&version=1.1.0&request=GetFeature&typeName=app:Bouwvlak&bbox="

xPathCadastre1 = ".//{http://www.opengis.net/gml/3.2}posList"
xPathCadastre2 = ".//{http://www.opengis.net/gml/3.2}pos"
xPathStringsCadastreTextAngle = [".//{http://kadastralekaartv4.geonovum.nl}hoek", ".//{http://kadastralekaartv4.geonovum.nl}tekst"]
xPathRuimtelijkePlannen = ".//{http://www.opengis.net/gml}posList"
xPathStrings3DBag = [".//{3dbag}ground-0.50", ".//{3dbag}roof-0.50"]
xPath3DBag3 = ".//{http://www.opengis.net/gml}posList"
#Xpath for several Web Feature Servers

GeoserviceLibrariesNetherlands = {"DutchGEOLuchtfoto2019WMS": DutchGEOLuchtfoto2019WMS,"DutchGEOCadastreServerRequest1":DutchGEOCadastreServerRequest1}

def GIS2BIM_GML_poslistData(tree, xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
#group X and Y Coordinates of polylines
    posLists = tree.findall(xPathString)
    xyPosList = []
    for posList in posLists:
        dataPosList = posList.text
        coordSplit = dataPosList.split()
        x = 0
        coordSplitXY = []
        for j in range(0, int(len(coordSplit) / XYZCountDimensions)):
            xy_coord = (round((float(coordSplit[x])+dx)*scale,DecimalNumbers), round((float(coordSplit[x+1])+dy)*scale,DecimalNumbers))
            coordSplitXY.append(xy_coord)
            x +=XYZCountDimensions
        xyPosList.append(coordSplitXY)
    return xyPosList

def GIS2BIM_CreateBoundingBox(CoordinateX,CoordinateY,BoxWidth,BoxHeight,DecimalNumbers):
#Create Boundingboxstring for use in webrequests.
    XLeft = round(CoordinateX-0.5*BoxWidth,DecimalNumbers)
    XRight = round(CoordinateX+0.5*BoxWidth,DecimalNumbers)
    YBottom = round(CoordinateY-0.5*BoxHeight,DecimalNumbers)
    YTop = round(CoordinateY+0.5*BoxHeight,DecimalNumbers)
    boundingBoxString = str(XLeft) + "," + str(YBottom) + "," + str(XRight) + "," + str(YTop)
    return boundingBoxString

def GIS2BIM_PointsFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
# group X and Y Coordinates
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = GIS2BIM_GML_poslistData(tree,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    return xyPosList

def GIS2BIM_DataFromWFS(serverName,boundingBoxString,xPathStringCoord,xPathStrings,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
# group textdata from WFS
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = GIS2BIM_GML_poslistData(tree,xPathStringCoord,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    xPathResults = []
    for xPathString in xPathStrings:
        a = tree.findall(xPathString)
        xPathResulttemp2 = []
        for xPathResult in a:
            xPathResulttemp2.append(xPathResult.text)
        xPathResults.append(xPathResulttemp2)
    xPathResults.insert(0,xyPosList)
    return xPathResults

## GIS2BIM within BLENDER

import urllib.request
import urllib
import xml.etree.ElementTree as ET
import json
import bpy
import bmesh

def GIS2BIM_BLENDER_CurvestoBlenderCurves(curves):
    blenderCurves = []
    for i in curves:
        verts = []
        for j in i:
            verts.append((j[0], j[1], 0))
        blenderCurves.append(verts)
    return blenderCurves

def GIS2BIM_BLENDER_add_mesh(name, verts, faces, edges=None, col_name="Collection"):    
    if edges is None:
        edges = []
    mesh = bpy.data.meshes.new(name) #mesh bouwen/vlak
    obj = bpy.data.objects.new(mesh.name, mesh) #create object
    col = bpy.data.collections.get(col_name) #Defineren/krijgen van de col
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh = mesh.from_pydata(verts, edges, faces)
    return mesh

def GIS2BIM_BLENDER_CurvesToMesh(BlenderCurves,Prefix):
    a = 0
    for i in BlenderCurves:
        a = a + 1 
        firstItem = i[0]
        i.append(firstItem) # closed polygon
        vlength = len(i)
        result = list(range(vlength))
        faces = [result]
        GIS2BIM_BLENDER_add_mesh(Prefix + str(a), i, faces)
    return faces

def GIS2BIM_BLENDER_PlaceText(textData,fontSize):
    for i, j, k in zip(textData[0], textData[1], textData[2]):
        loc_txt = bpy.data.curves.new(type="FONT",name="txt") 
        loc_txt.body = k
        loc_obj = bpy.data.objects.new("GIS2BIM-text", loc_txt)
        loc_obj.location = (i[0][0], i[0][1], 0)
        bpy.context.scene.collection.objects.link(loc_obj)
    return loc_obj   

crsx = bpy.data.scenes["Scene"].get("crs x", "fallback value")
crsy = bpy.data.scenes["Scene"].get("crs y", "fallback value")
latitude = bpy.data.scenes["Scene"].get("latitude", "fallback value")
longitude = bpy.data.scenes["Scene"].get("longitude", "fallback value")

Rdx = crsx
Rdy = crsy
width = 500
height = 500
scalefactor = 1.6

Bbox = GIS2BIM_CreateBoundingBox(Rdx,Rdy,width,height,2)

BAGcurves = GIS2BIM_PointsFromWFS(DutchGEOBAG,Bbox,xPathCadastre1,-Rdx,-Rdy,scalefactor,3,2)

textDataCadastralParcels = GIS2BIM_DataFromWFS(DutchGEOCadastreServerRequest2,Bbox,xPathCadastre2,xPathStringsCadastreTextAngle,-Rdx,-Rdy,scalefactor,3,2)
textDataOpenbareRuimtenaam = GIS2BIM_DataFromWFS(DutchGEOCadastreServerRequest3,Bbox,xPathCadastre2,xPathStringsCadastreTextAngle,-Rdx,-Rdy,scalefactor,3,2)

#BAGSurface = GIS2BIM_BLENDER_CurvesToMesh(GIS2BIM_BLENDER_CurvestoBlenderCurves(BAGcurves),'BAG')
#placeBlenderTextCadastralParcels = GIS2BIM_BLENDER_PlaceText(textDataCadastralParcels,50)
#placeBlenderTextOpenbareRuimtenaam = GIS2BIM_BLENDER_PlaceText(textDataOpenbareRuimtenaam,50)


def GIS2BIM_BLENDER_add_mesh(name, verts, faces, edges=None, col_name="Collection"):    
    if edges is None:
        edges = []
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get(col_name)
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)

def GIS2BIM_BLENDER_draw_line(Coordinate1, Coordinate2, Name):
    #Name is string
    #Coordinate is list of 3 floats
    verts = [Coordinate1,Coordinate2,]
    vlength = len(verts)
    result = list(range(vlength))   
    faces = [result]
    GIS2BIM_BLENDER_add_mesh(Name, verts, faces)

C1 = (1000.0,  5000.0,  0.0)
C2 = (0, 0, 0)

GIS2BIM_BLENDER_draw_line(C1,C2,"test")