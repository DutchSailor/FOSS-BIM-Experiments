## GIS2BIM Library

## GIS2BIM within BLENDER

import urllib.request
import urllib
import xml.etree.ElementTree as ET
import json
import bpy
import bmesh

crsx = bpy.data.scenes["Scene"].get("crs x", "fallback value")
crsy = bpy.data.scenes["Scene"].get("crs y", "fallback value")
latitude = bpy.data.scenes["Scene"].get("latitude", "fallback value")
longitude = bpy.data.scenes["Scene"].get("longitude", "fallback value")

def CurvestoBlenderCurves(curves):
    blenderCurves = []
    for i in curves:
        verts = []
        for j in i:
            verts.append((j[0], j[1], 0))
        blenderCurves.append(verts)
    return blenderCurves

def add_mesh(name, verts, faces, edges=None, col_name="Collection"):    
    if edges is None:
        edges = []
    mesh = bpy.data.meshes.new(name) #mesh bouwen/vlak
    obj = bpy.data.objects.new(mesh.name, mesh) #create object
    col = bpy.data.collections.get(col_name) #Defineren/krijgen van de col
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh = mesh.from_pydata(verts, edges, faces)
    return mesh

def CurvesToMesh(BlenderCurves,Prefix):
    a = 0
    for i in BlenderCurves:
        a = a + 1 
        firstItem = i[0]
        i.append(firstItem) # closed polygon
        vlength = len(i)
        result = list(range(vlength))
        faces = [result]
        add_mesh(Prefix + str(a), i, faces)
    return faces

def PlaceText(textData,fontSize):
    for i, j, k in zip(textData[0], textData[1], textData[2]):
        loc_txt = bpy.data.curves.new(type="FONT",name="txt") 
        loc_txt.body = k
        loc_obj = bpy.data.objects.new("snapGIS-text", loc_txt)
        loc_obj.location = (i[0][0], i[0][1], 0)
        bpy.context.scene.collection.objects.link(loc_obj)
    return loc_obj   