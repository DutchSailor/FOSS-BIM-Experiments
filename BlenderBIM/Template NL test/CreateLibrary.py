# BlenderBIM Add-on - OpenBIM Blender Add-on
# Copyright (C) 2020, 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of BlenderBIM Add-on.
#
# BlenderBIM Add-on is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.

# 2023-08-10: Modified by Maarten Vroegindeweij
# documentation: 
    #  https://blenderbim.org/docs-python/autoapi/ifcopenshell/api/material/add_material_set/index.html
    #  https://wiki.osarch.org/index.php?title=IFC_-_Industry_Foundation_Classes/IFC_materials
    #  https://academy.ifcopenshell.org/
import bpy
import ifcopenshell
import ifcopenshell.api
import blenderbim.tool as tool
import sys
import pandas as pd
import numpy
import pandas_ods_reader
from pandas_ods_reader import read_ods
import uuid

#for grids
import blenderbim.core.spatial
import blenderbim.tool as tool
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty
from mathutils import Vector
from blenderbim.bim.ifc import IfcStore

#FUNCTIONS

def create_line_type(self, name, classes):
    element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcTypeProduct", name=name)
    element.ApplicableOccurrence = "IfcAnnotation/LINEWORK"
    pset = ifcopenshell.api.run("pset.add_pset", self.file, product=element, name="EPset_Annotation")
    ifcopenshell.api.run("pset.edit_pset", self.file, pset=pset, properties={"Classes": classes})

def create_text_type(self, name, symbol, literals):
    element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcTypeProduct", name=name)
    element.ApplicableOccurrence = "IfcAnnotation/TEXT"
    pset = ifcopenshell.api.run("pset.add_pset", self.file, product=element, name="EPset_Annotation")
    ifcopenshell.api.run("pset.edit_pset", self.file, pset=pset, properties={"Symbol": symbol})
    items = []
    for literal in literals:
        origin = self.file.createIfcAxis2Placement3D(
            self.file.createIfcCartesianPoint((0.0, 0.0, 0.0)),
            self.file.createIfcDirection((0.0, 0.0, 1.0)),
            self.file.createIfcDirection((1.0, 0.0, 0.0)),
        )
        items.append(self.file.createIfcTextLiteralWithExtent(
            literal, origin, "RIGHT", self.file.createIfcPlanarExtent(1000, 1000), "center"
        ))

    representation = self.file.createIfcShapeRepresentation(
        self.representations["plan_annotation"],
        self.representations["plan_annotation"].ContextIdentifier,
        "Annotation2D",
        items,
    )
    ifcopenshell.api.run(
        "geometry.assign_representation", self.file, product=element, representation=representation
    )

def create_layer_type(self, ifc_class, name, description, thickness, material_element):
    element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class=ifc_class, name=name)
    rel = ifcopenshell.api.run("material.assign_material", self.file, product=element, type="IfcMaterialLayerSet")
    layer_set = rel.RelatingMaterial
    layer = ifcopenshell.api.run("material.add_layer", self.file, layer_set=layer_set, material=material_element)
    layer.LayerThickness = thickness
    ifcopenshell.api.run("project.assign_declaration", self.file, definition=element, relating_context=self.library)
    return element

def create_profile_type(self, ifc_class, name, profile, material_element):
    element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class=ifc_class, name=name)
    rel = ifcopenshell.api.run("material.assign_material", self.file, product=element, type="IfcMaterialProfileSet")
    profile_set = rel.RelatingMaterial
    material_profile = ifcopenshell.api.run(
        "material.add_profile", self.file, profile_set=profile_set, material=material_element
    )
    ifcopenshell.api.run("material.assign_profile", self.file, material_profile=material_profile, profile=profile)
    ifcopenshell.api.run("project.assign_declaration", self.file, definition=element, relating_context=self.library)

def create_type(self, ifc_class, name, representations):
    element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class=ifc_class, name=name)
    for rep_name, obj_name in representations.items():
        obj = bpy.data.objects.get(obj_name)
        representation = ifcopenshell.api.run(
            "geometry.add_representation",
            self.file,
            context=self.representations[rep_name],
            blender_object=obj,
            geometry=obj.data,
            total_items=max(1, len(obj.material_slots)),
        )
        styles = []
        for slot in obj.material_slots:
            style = ifcopenshell.api.run("style.add_style", self.file, name=slot.material.name)
            ifcopenshell.api.run(
                "style.add_surface_style",
                self.file,
                style=style,
                ifc_class="IfcSurfaceStyleShading",
                attributes=tool.Style.get_surface_shading_attributes(slot.material),
            )
            styles.append(style)
        if styles:
            ifcopenshell.api.run(
                "style.assign_representation_styles", self.file, shape_representation=representation, styles=styles
            )
        ifcopenshell.api.run(
            "geometry.assign_representation", self.file, product=element, representation=representation
        )
    ifcopenshell.api.run("project.assign_declaration", self.file, definition=element, relating_context=self.library)
    
#INPUT
path = "C:/BlenderBIM/3bm/Standards test folder/Library.ods"
templatepath = "C:/BlenderBIM/3bm/Standards test folder/IFC4 3BM Demo Template 0.2.ifc"
projectname = "BlenderBIM 3BM ProjectTemplate 0.2"
libraryname = "BlenderBIM 3BM Library 0.2"


#CREATE IFC FILE
ifcopenshell.api.pre_listeners = {}
ifcopenshell.api.post_listeners = {}
    
create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)

ifcfile = ifcopenshell.api.run("project.create_file")
self.project = ifcopenshell.api.run(
    "root.create_entity", ifcfile, ifc_class="IfcProject", name=filename)
    
self.library = ifcopenshell.api.run(
    "root.create_entity", ifcfile, ifc_class="IfcProjectLibrary", name=libraryname)
    
ifcopenshell.api.run(
    "project.assign_declaration", ifcfile, definition=self.library, relating_context=self.project)

site_placement = create_ifclocalplacement(ifcfile)
site = ifcfile.createIfcSite(create_guid(), "site", None, None, site_placement, None, None, "ELEMENT", None, None, None, None, None)

container_site = ifcfile.createIfcRelAggregates(create_guid(), "Site Container", None, site, [building])
container_project = ifcfile.createIfcRelAggregates(create_guid(), "Project Container", None, project, [site])

ifcopenshell.api.run("unit.assign_unit", ifcfile, length={"is_metric": True, "raw": "MILLIMETERS"}) #METERS OR MILLIMETERS
model = ifcopenshell.api.run("context.add_context", ifcfile, context_type="Model")
plan = ifcopenshell.api.run("context.add_context", ifcfile, context_type="Plan")
self.representations = {
    "model_body": ifcopenshell.api.run(
        "context.add_context",
        ifcfile,
        context_type="Model",
        context_identifier="Body",
        target_view="MODEL_VIEW",
        parent=model,
    ),
    "plan_body": ifcopenshell.api.run(
        "context.add_context",
        ifcfile,
        context_type="Plan",
        context_identifier="Body",
        target_view="PLAN_VIEW",
        parent=plan,
    ),
    "plan_annotation": ifcopenshell.api.run(
        "context.add_context",
        ifcfile,
        context_type="Plan",
        context_identifier="Annotation",
        target_view="PLAN_VIEW",
        parent=plan,
    ),
}
    
#0 ORGANISATION DETAILS
organisation = ifcfile.createIfcOrganization()
organisation.Name = "BlenderBIM NL I.O."

person = ifcfile.createIfcPerson()
person.FamilyName = "M.D. Vroegindeweij"

#0 MATERIALS

#0.1 MATERIAL PROFILE SETS


sheet_name = "materials"
library_mat = read_ods(path, sheet_name)

for ind in library_mat.index:
    material_name = library_mat["IfcElementType"][ind]
    style_name = library_mat["IfcElementType"][ind] + "_S"
    material_category = library_mat["Category"][ind]
    rgb = library_mat["RGB"][ind]
    red = float(rgb.split(',')[0])/51
    green = float(rgb.split(',')[1])/51
    blue = float(rgb.split(',')[2])/51
    
    material_obj = globals()[material_name] = ifcopenshell.api.run("material.add_material", ifcfile, name=material_name, category=material_category)
    
    context = ifcfile.createIfcGeometricRepresentationContext()
    style = ifcopenshell.api.run("style.add_style", ifcfile, name=style_name)
    
    ifcopenshell.api.run("style.add_surface_style", ifcfile,
    style=style, ifc_class="IfcSurfaceStyleShading", attributes={
        "SurfaceColour": { "Name": style_name, "Red": red, "Green": green, "Blue": blue },
        "Transparency": 0., # 0 is opaque, 1 is transparent
    })
    ifcopenshell.api.run(
        "style.assign_material_style",
        ifcfile,
        material=material_obj,
        style=style,
        context=context,
    )

#1 WALL TYPES SINGLE LAYER
sheet_name = "walls_single_layer"
library_walls = read_ods(path, sheet_name)

for ind in library_walls.index:
    wall_name = library_walls["Name"][ind]
    wall_thickness = float(library_walls["Thickness"][ind])
    wall_description = library_walls["Description"][ind]
    wall_material = library_walls["Material"][ind] 
    wall_material_var = globals()[wall_material]
    self.create_layer_type("IfcWallType", wall_name, wall_description, wall_thickness, wall_material_var) #create wall type


#2 FLOOR TYPES SINGLE LAYER
sheet_name = "floors_single_layer"
library_floors = read_ods(path, sheet_name)

for ind in library_floors.index:
    floor_name = library_floors["Name"][ind]
    floor_thickness = float(library_floors["Thickness"][ind])
    floor_description = library_floors["Description"][ind]
    floor_material = library_floors["Material"][ind] 
    floor_material_var = globals()[floor_material]
    self.create_layer_type("IfcSlabType", floor_name, floor_description, floor_thickness, floor_material_var) #create floor type


#3 RECTANGLE PROFILES, BEAMS, COLUMNS
sheet_name = "profiles_rect"
library_rectprofile = read_ods(path, sheet_name)

for ind in library_rectprofile.index:
    profile_name = library_rectprofile["Name"][ind]
    profile_width = float(library_rectprofile["Width"][ind])
    profile_height = float(library_rectprofile["Height"][ind])
    profile_material = library_rectprofile["Material"][ind]
    profile_material_var = globals()[profile_material]
    make_column = library_rectprofile["MakeIfcColumnType"][ind]
    make_beam = library_rectprofile["MakeIfcBeamType"][ind]
    profile = ifcfile.create_entity("IfcRectangleProfileDef", ProfileName=profile_name, ProfileType="AREA", XDim=profile_width, YDim=profile_height) # profile
    if make_column is True:
        self.create_profile_type("IfcColumnType", profile_name, profile, profile_material_var)
    if make_beam is True:
        self.create_profile_type("IfcBeamType", profile_name, profile, profile_material_var)

#4 ROUND PROFILES, BEAMS, COLUMNS
sheet_name = "profiles_round"
library_roundprofile = read_ods(path, sheet_name)

for ind in library_roundprofile.index:
    profile_name = library_roundprofile["Name"][ind]
    profile_radius = float(library_roundprofile["Radius"][ind])
    profile_material = library_roundprofile["Material"][ind]
    profile_material_var = globals()[profile_material]
    make_column = library_roundprofile["MakeIfcColumnType"][ind]
    make_beam = library_roundprofile["MakeIfcBeamType"][ind]
    profile = ifcfile.create_entity("IfcCircleProfileDef", ProfileName=profile_name, ProfileType="AREA", Radius=profile_width) # profile
    if make_column is True:
        self.create_profile_type("IfcColumnType", profile_name, profile, profile_material_var)
    if make_beam is True:
        self.create_profile_type("IfcBeamType", profile_name, profile, profile_material_var)
        
        
self.create_line_type("DASHED", "dashed")
self.create_line_type("FINE", "fine")
self.create_line_type("THIN", "thin")
self.create_line_type("MEDIUM", "medium")
self.create_line_type("THICK", "thick")
self.create_line_type("STRONG", "strong")
self.create_text_type("DOOR-TAG", "door-tag", ["{{type.Name}}", "{{Name}}"])
self.create_text_type("WINDOW-TAG", "window-tag", ["{{Name}}"])
self.create_text_type("SPACE-TAG", "space-tag", ["{{Name}}", "{{Description}}", "``round({{Qto_SpaceBaseQuantities.NetFloorArea}} or 0., 2)``"])
self.create_text_type("MATERIAL-TAG", "rectangle-tag", ["{{material.Name}}"])
self.create_text_type("TYPE-TAG", "capsule-tag", ["{{type.Name}}"])
self.create_text_type("NAME-TAG", "capsule-tag", ["{{Name}}"])

ifcfile.write(templatepath)

def create_line_type(self, name, classes):
    element = ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcTypeProduct", name=name)
    element.ApplicableOccurrence = "IfcAnnotation/LINEWORK"
    pset = ifcopenshell.api.run("pset.add_pset", ifcfile, product=element, name="EPset_Annotation")
    ifcopenshell.api.run("pset.edit_pset", ifcfile, pset=pset, properties={"Classes": classes})

def create_text_type(self, name, symbol, literals):
    element = ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class="IfcTypeProduct", name=name)
    element.ApplicableOccurrence = "IfcAnnotation/TEXT"
    pset = ifcopenshell.api.run("pset.add_pset", ifcfile, product=element, name="EPset_Annotation")
    ifcopenshell.api.run("pset.edit_pset", ifcfile, pset=pset, properties={"Symbol": symbol})
    items = []
    for literal in literals:
        origin = ifcfile.createIfcAxis2Placement3D(
            ifcfile.createIfcCartesianPoint((0.0, 0.0, 0.0)),
            ifcfile.createIfcDirection((0.0, 0.0, 1.0)),
            ifcfile.createIfcDirection((1.0, 0.0, 0.0)),
        )
        items.append(ifcfile.createIfcTextLiteralWithExtent(
            literal, origin, "RIGHT", ifcfile.createIfcPlanarExtent(1000, 1000), "center"
        ))

    representation = ifcfile.createIfcShapeRepresentation(
        self.representations["plan_annotation"],
        self.representations["plan_annotation"].ContextIdentifier,
        "Annotation2D",
        items,
    )
    ifcopenshell.api.run(
        "geometry.assign_representation", ifcfile, product=element, representation=representation
    )

def create_layer_type(self, ifc_class, name, description, thickness, material_element):
    element = ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class=ifc_class, name=name)
    rel = ifcopenshell.api.run("material.assign_material", ifcfile, product=element, type="IfcMaterialLayerSet")
    layer_set = rel.RelatingMaterial
    layer = ifcopenshell.api.run("material.add_layer", ifcfile, layer_set=layer_set, material=material_element)
    layer.LayerThickness = thickness
    ifcopenshell.api.run("project.assign_declaration", ifcfile, definition=element, relating_context=self.library)
    return element

def create_profile_type(self, ifc_class, name, profile, material_element):
    element = ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class=ifc_class, name=name)
    rel = ifcopenshell.api.run("material.assign_material", ifcfile, product=element, type="IfcMaterialProfileSet")
    profile_set = rel.RelatingMaterial
    material_profile = ifcopenshell.api.run(
        "material.add_profile", ifcfile, profile_set=profile_set, material=material_element
    )
    ifcopenshell.api.run("material.assign_profile", ifcfile, material_profile=material_profile, profile=profile)
    ifcopenshell.api.run("project.assign_declaration", ifcfile, definition=element, relating_context=self.library)

def create_type(self, ifc_class, name, representations):
    element = ifcopenshell.api.run("root.create_entity", ifcfile, ifc_class=ifc_class, name=name)
    for rep_name, obj_name in representations.items():
        obj = bpy.data.objects.get(obj_name)
        representation = ifcopenshell.api.run(
            "geometry.add_representation",
            ifcfile,
            context=self.representations[rep_name],
            blender_object=obj,
            geometry=obj.data,
            total_items=max(1, len(obj.material_slots)),
        )
        styles = []
        for slot in obj.material_slots:
            style = ifcopenshell.api.run("style.add_style", ifcfile, name=slot.material.name)
            ifcopenshell.api.run(
                "style.add_surface_style",
                ifcfile,
                style=style,
                ifc_class="IfcSurfaceStyleShading",
                attributes=tool.Style.get_surface_shading_attributes(slot.material),
            )
            styles.append(style)
        if styles:
            ifcopenshell.api.run(
                "style.assign_representation_styles", ifcfile, shape_representation=representation, styles=styles
            )
        ifcopenshell.api.run(
            "geometry.assign_representation", ifcfile, product=element, representation=representation
        )
    ifcopenshell.api.run("project.assign_declaration", ifcfile, definition=element, relating_context=self.library)

#2 CREATE GRID
polylineSet = []
gridX = []
gridY = []

#GRID X
point_1 = ifcfile.createIfcCartesianPoint((0,-2000))
point_2 = ifcfile.createIfcCartesianPoint((0, 15000))

Line = ifcfile.createIfcPolyline( [point_1 , point_2] )
polylineSet.append(Line)

grid = ifcfile.createIfcGridAxis()
grid.AxisTag = "A"
grid.AxisCurve = Line
grid.SameSense = True
gridX.append(grid)

#GRID Y
point_1 = ifcfile.createIfcCartesianPoint((x_min_overlap,i_grid[1]))
point_2 = ifcfile.createIfcCartesianPoint((x_max_overlap,i_grid[1]))

Line = ifcfile.createIfcPolyline( [point_1 , point_2] )
polylineSet.append(Line)

grid = ifcfile.createIfcGridAxis()
grid.AxisTag = str(i_grid[0]) + "Y"
grid.AxisCurve = Line
grid.SameSense = True
gridY.append(grid)
      
# Defining the grid 
PntGrid = ifcfile.createIfcCartesianPoint( O )

myGridCoordinateSystem = ifcfile.createIfcAxis2Placement3D()
myGridCoordinateSystem.Location= PntGrid
myGridCoordinateSystem.Axis = axis_Z
myGridCoordinateSystem.RefDirection = axis_X

grid_placement = ifcfile.createIfcLocalPlacement()
grid_placement.PlacementRelTo = storey_placement
grid_placement.RelativePlacement = myGridCoordinateSystem

grid_curvedSet =  ifcfile.createIfcGeometricCurveSet(polylineSet)

gridShape_Reppresentation = ifcfile.createIfcShapeRepresentation()
gridShape_Reppresentation.ContextOfItems = footprint_context
gridShape_Reppresentation.RepresentationIdentifier = 'FootPrint'
gridShape_Reppresentation.RepresentationType = 'GeometricCurveSet'
gridShape_Reppresentation.Items = [grid_curvedSet]

grid_Representation = ifcfile.createIfcProductDefinitionShape()
grid_Representation.Representations  = [gridShape_Reppresentation]

myGrid = ifcfile.createIfcGrid(create_guid() , owner_history)
myGrid.ObjectPlacement = grid_placement
myGrid.Representation = grid_Representation
myGrid.UAxes=gridX
myGrid.VAxes=gridY

container_SpatialStructure= ifcfile.createIfcRelContainedInSpatialStructure(create_guid() , owner_history)
container_SpatialStructure.Name='BuildingStoreyContainer'
container_SpatialStructure.Description = 'BuildingStoreyContainer for Elements'
container_SpatialStructure.RelatingStructure = site
container_SpatialStructure.RelatedElements = [myGrid]