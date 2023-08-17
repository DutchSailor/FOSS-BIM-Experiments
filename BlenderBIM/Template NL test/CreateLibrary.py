# CODE PIECES USED OF DION MOULT
# CODE PIECES USED OF COEN  CLAUS
# 2023-08-16: Modified by Maarten Vroegindeweij
# documentation:
#  https://blenderbim.org/docs-python/autoapi/ifcopenshell/api/material/add_material_set/index.html
#  https://wiki.osarch.org/index.php?title=IFC_-_Industry_Foundation_Classes/IFC_materials
#  https://academy.ifcopenshell.org/

import bpy
import blenderbim.tool as tool
from blenderbim.bim.ifc import IfcStore
import blenderbim.core.drawing as drawing
import ifcopenshell
import ifcopenshell.api
import sys
import pandas as pd
import numpy
import pandas_ods_reader
from pandas_ods_reader import read_ods
import uuid
from collections import OrderedDict
import time

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.
create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)


path = "C:/Users/mikev/Documents/GitHub/FOSS-BIM-Experiments/BlenderBIM/Template NL test/Library.ods"
library_path = "C:/Users/mikev/Documents/GitHub/FOSS-BIM-Experiments/BlenderBIM/Template NL test/IFC4 NL Demo Library 0.2.ifc"

building_storeys_lst = [
    ["ok fundering", -800],
    ["bk fundering", -400],
    ["peil=00",0],
    ["BWK_01",2840],
    ["BWK_02",5680]
    ]

class LibraryGenerator:
    def generate(self):
        ifcopenshell.api.pre_listeners = {}
        ifcopenshell.api.post_listeners = {}

        # CREATE PROJECT FILE & LIBRARY
        self.file = ifcopenshell.api.run("project.create_file")
        self.project = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcProject", name="BlenderBIM NL Library_Template Proof of Concept v0_2")
        self.library = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcProjectLibrary", name="BlenderBIM NL Library_Template Proof of Concept v0_2")
        library = ifcopenshell.api.run("project.assign_declaration", self.file, definition=self.library, relating_context=self.project)
        units = ifcopenshell.api.run("unit.assign_unit", self.file,length={"is_metric": True, "raw": "MILLIMETERS"})  # METERS OR MILLIMETERS

        #HELPERS CREATE AXIS
        self.axis_X = self.file.createIfcDirection(X)
        self.axis_Y = self.file.createIfcDirection(Y)
        self.axis_Z = self.file.createIfcDirection(Z)
        self.Pnt_O = self.file.createIfcCartesianPoint(O)

        # REPRESENTATIONS ETC

        model = ifcopenshell.api.run("context.add_context", self.file, context_type="Model")
        plan = ifcopenshell.api.run("context.add_context", self.file, context_type="Plan")

        self.representations = {
            "model_body": ifcopenshell.api.run(
                "context.add_context",
                self.file,
                context_type="Model",
                context_identifier="Body",
                target_view="MODEL_VIEW",
                parent=model,
            ),
            "plan_body": ifcopenshell.api.run(
                "context.add_context",
                self.file,
                context_type="Plan",
                context_identifier="Body",
                target_view="PLAN_VIEW",
               parent=plan,
            ),
            "plan_annotation": ifcopenshell.api.run(
                "context.add_context",
                self.file,
                context_type="Plan",
                context_identifier="Annotation",
                target_view="PLAN_VIEW",
                parent=plan,
            ),
        }

        model_body = self.representations["model_body"]
        #context = model_body
        self.footprint_context = model_body

        # ORGANISATION DETAILS
        organisation = self.file.createIfcOrganization()
        organisation.Name = "BlenderBIM NL io"

        person = self.file.createIfcPerson()
        person.FamilyName = "M.D. Vroegindeweij"

        # APPLICATION
        app = self.file.createIfcApplication()
        app.ApplicationDeveloper = organisation
        app.Version = "0.7"
        app.ApplicationFullName = "IfcOpenShell v0.7.0-1b1fd1e6"

        # OWNER HISTORY
        self.owner_history = self.file.createIfcOwnerHistory()
        self.owner_history.OwningUser = person
        self.owner_history.OwningApplication = app
        self.owner_history.ChangeAction = "NOCHANGE"
        self.owner_history.CreationDate = int(time.time())

        # CREATE THE SITE
        site_placement = self.create_ifclocalplacement()

        #self.site = self.file.createIfcSite(create_guid(), self.owner_history, "site", None, None, site_placement, None, None,
        #                             "ELEMENT", None, None, None, None, None)

        # CREATE THE BUILDING
        building_placement = self.create_ifclocalplacement(O,Z,X,site_placement)
        #building = self.file.createIfcBuilding(create_guid(), self.owner_history, 'Bouwwerk', None, None,building_placement, None, None, "ELEMENT", None, None, None)

        self.site = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcSite", name="Site")
        self.building = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcBuilding", name="Gebouw")

        # Since the site is our top level location, assign it to the project
        # Then place our building on the site, and our storey in the building
        ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.project, product=self.site)
        ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.site, product=self.building)

        #container_site = self.file.createIfcRelAggregates(create_guid(), self.owner_history, "Site Container", None, self.site,[building])
        #container_project = self.file.createIfcRelAggregates(create_guid(), self.owner_history, "Project Container",None, self.project,[self.site])

        # CREATE BUILDING STOREYS
        self.storey_placement = self.create_ifclocalplacement(O,Z,X,relative_to=building_placement)
        storeys_obj = self.create_building_storeys(building_storeys_lst)
        storey = storeys_obj[2]
        #storey = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcBuildingStorey", name="peil=0")
        ifcopenshell.api.run("aggregate.assign_object", self.file, relating_object=self.building, product=storey)

        # CREATE GRID
        self.create_grid(5400,6000,5,5,2000)

        # 0 MATERIALS

        # 0.1 MATERIAL PROFILE SETS

        sheet_name = "materials"
        library_mat = read_ods(path, sheet_name)

        for ind in library_mat.index:
            material_name = library_mat["IfcElementType"][ind]
            style_name = library_mat["IfcElementType"][ind] + "_S"
            material_category = library_mat["Category"][ind]
            rgb = library_mat["RGB"][ind]
            red = float(rgb.split(',')[0]) / 51
            green = float(rgb.split(',')[1]) / 51
            blue = float(rgb.split(',')[2]) / 51

            material_obj = globals()[material_name] = ifcopenshell.api.run("material.add_material", self.file,
                                                                           name=material_name,
                                                                           category=material_category)

            context = self.file.createIfcGeometricRepresentationContext()
            style = ifcopenshell.api.run("style.add_style", self.file, name=style_name)

            ifcopenshell.api.run("style.add_surface_style", self.file,
                                 style=style, ifc_class="IfcSurfaceStyleShading", attributes={
                    "SurfaceColour": {"Name": style_name, "Red": red, "Green": green, "Blue": blue},
                    "Transparency": 0.,  # 0 is opaque, 1 is transparent
                })
            ifcopenshell.api.run(
                "style.assign_material_style",
                self.file,
                material=material_obj,
                style=style,
                context=context,
            )

        # 1 WALL TYPES SINGLE LAYER
        sheet_name = "walls_single_layer"
        library_walls = read_ods(path, sheet_name)
        y = 0
        length = 1 #m
        height = 2.85 #m
        spacing_walls = 0.5 #m
        for ind in library_walls.index:
            wall_name = library_walls["Name"][ind]
            wall_thickness = float(library_walls["Thickness"][ind])
            wall_description = library_walls["Description"][ind]
            wall_material = library_walls["Material"][ind]
            wall_material_var = globals()[wall_material]
            wall_type = self.create_layer_type("IfcWallType", wall_name, wall_description, wall_thickness,
                                   wall_material_var, wall_material)  # create wall type

            place_wall = self.place_wall(wall_name, wall_type, model_body, wall_thickness, length, height, 0, y, 0, storey)
            y = y + spacing_walls


        # 2 FLOOR TYPES SINGLE LAYER
        sheet_name = "floors_single_layer"
        library_floors = read_ods(path, sheet_name)

        length = 500
        width = 500
        x = 1500
        y = 0
        spacing = 500
        for ind in library_floors.index:
            floor_name = library_floors["Name"][ind]
            floor_thickness = float(library_floors["Thickness"][ind])
            floor_description = library_floors["Description"][ind]
            floor_material = library_floors["Material"][ind]
            floor_material_var = globals()[floor_material]
            slab_type = self.create_layer_type("IfcSlabType", floor_name, floor_description, floor_thickness,
                                   floor_material_var, floor_material)  # create floor type

            #PLACE SLAB
            place_slab = self.place_slab(storey, slab_type, length, width, floor_thickness, x, y, model_body, floor_name, floor_description)
            y = y + spacing

        # 3 RECTANGLE PROFILES, BEAMS, COLUMNS
        sheet_name = "profiles_rect"
        library_rectprofile = read_ods(path, sheet_name)

        column_height = 3
        beam_length = 2
        x = 4
        y = 0
        z = 0
        spacing = 0.7
        x2 = 7
        y2 = 0
        for ind in library_rectprofile.index:
            profile_name = library_rectprofile["Name"][ind]
            profile_width = float(library_rectprofile["Width"][ind])
            profile_height = float(library_rectprofile["Height"][ind])
            profile_material = library_rectprofile["Material"][ind]
            profile_material_var = globals()[profile_material]
            make_column = library_rectprofile["MakeIfcColumnType"][ind]
            make_beam = library_rectprofile["MakeIfcBeamType"][ind]
            profile_type_obj = self.file.create_entity("IfcRectangleProfileDef", ProfileName=profile_name, ProfileType="AREA",
                                              XDim=profile_width, YDim=profile_height)  # profile
            if make_column is True:
                column_type_obj = self.create_profile_type("IfcColumnType", profile_name, profile_type_obj, profile_material_var)
                self.place_column(storey, column_type_obj, profile_type_obj, x, y, z, model_body, profile_name, column_height)
                y = y + spacing
            if make_beam is True:
                beam_type_obj = self.create_profile_type("IfcBeamType", profile_name, profile_type_obj, profile_material_var)
                self.place_beam(storey, beam_type_obj, profile_type_obj, x2, y2, z, model_body, profile_name, beam_length)
                y2 = y2 + spacing


        # 4 ROUND PROFILES, BEAMS, COLUMNS
        sheet_name = "profiles_round"
        library_roundprofile = read_ods(path, sheet_name)

        x = 6
        y = 0
        z = 0
        spacing = 0.7
        x2 = 11
        y2 = 0

        for ind in library_roundprofile.index:
            profile_name = library_roundprofile["Name"][ind]
            profile_radius = float(library_roundprofile["Radius"][ind])
            profile_material = library_roundprofile["Material"][ind]
            profile_material_var = globals()[profile_material]
            make_column = library_roundprofile["MakeIfcColumnType"][ind]
            make_beam = library_roundprofile["MakeIfcBeamType"][ind]
            profile_type_obj = self.file.create_entity("IfcCircleProfileDef", ProfileName=profile_name, ProfileType="AREA",
                                              Radius=profile_radius)  # profile
            if make_column is True:
                column_type_obj = self.create_profile_type("IfcColumnType", profile_name, profile_type_obj, profile_material_var)
                self.place_column(storey, column_type_obj, profile_type_obj, x, y, z, model_body, profile_name, column_height)
                y = y + spacing
            if make_beam is True:
                beam_type_obj = self.create_profile_type("IfcBeamType", profile_name, profile_type_obj, profile_material_var)
                self.place_beam(storey, beam_type_obj, profile_type_obj, x2, y2, z, model_body, profile_name, beam_length)
                y2 = y2 + spacing

        self.create_line_type("DASHED", "dashed")
        self.create_line_type("FINE", "fine")
        self.create_line_type("THIN", "thin")
        self.create_line_type("MEDIUM", "medium")
        self.create_line_type("THICK", "thick")
        self.create_line_type("STRONG", "strong")
        self.create_text_type("DOOR-TAG", "door-tag", ["{{type.Name}}", "{{Name}}"])
        self.create_text_type("WALL-TAG", "wall-tag", ["{{type.Name}}"])
        self.create_text_type("SLAB-TAG", "slab-tag", ["{{type.Name}}"])
        self.create_text_type("WINDOW-TAG", "window-tag", ["{{Name}}"])
        self.create_text_type("SPACE-TAG", "space-tag", ["{{Name}}", "{{Description}}",
                                                         "``round({{Qto_SpaceBaseQuantities.NetFloorArea}} or 0., 2)``"])
        self.create_text_type("MATERIAL-TAG", "rectangle-tag", ["{{material.Name}}"])
        self.create_text_type("TYPE-TAG", "capsule-tag", ["{{type.Name}}"])
        self.create_text_type("NAME-TAG", "capsule-tag", ["{{Name}}"])

        self.file.write(library_path)
        #self.load_ifc_automatically()
        #self.add_drawing()

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
                literal, origin, "RIGHT", self.file.createIfcPlanarExtent(500, 500), "left"
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

    def create_layer_type(self, ifc_class, name, description, thickness, material_element, material_layerset_name):
        element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class=ifc_class, name=name)
        element.Description = description
        rel = ifcopenshell.api.run("material.assign_material", self.file, product=element, type="IfcMaterialLayerSet")
        layer_set = rel.RelatingMaterial
        layer_set.LayerSetName = material_layerset_name
        layer_set.Description = description
        layer = ifcopenshell.api.run("material.add_layer", self.file, layer_set=layer_set, material=material_element)
        layer.LayerThickness = thickness
        ifcopenshell.api.run("project.assign_declaration", self.file, definition=element, relating_context=self.library)
        return element

    def create_profile_type(self, ifc_class, name, profile, material_element):
        element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class=ifc_class, name=name)
        rel = ifcopenshell.api.run("material.assign_material", self.file, product=element, type="IfcMaterialProfileSet")
        profile_set = rel.RelatingMaterial
        profile_set.Name = name
        material_profile = ifcopenshell.api.run(
            "material.add_profile", self.file, profile_set=profile_set, material=material_element
        )
        ifcopenshell.api.run("material.assign_profile", self.file, material_profile=material_profile, profile=profile)
        ifcopenshell.api.run("project.assign_declaration", self.file, definition=element, relating_context=self.library)
        return element

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

    def place_wall(self, wall_name, wall_type_obj, model_body, wall_thickness, length, height, x, y, z, building_storey_obj):
        ifc_wall_type_instance = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcWall",
                                                      name=wall_name)
        ifcopenshell.api.run("type.assign_type", self.file, related_object=ifc_wall_type_instance,
                             relating_type=wall_type_obj)

        representation = ifcopenshell.api.run("geometry.add_wall_representation", self.file, context=model_body,
                                              length=length, height=height,
                                              thickness=wall_thickness / 1000, name=wall_name)

        matrix_1 = numpy.array(
            (
                (1.0, 0.0, 0.0, x),
                (0.0, 1.0, 0.0, y),
                (0.0, 0.0, 1.0, z),
                (0.0, 0.0, 0.0, 1.0),
            )
        )
        ifcopenshell.api.run("type.assign_type", self.file, related_object=ifc_wall_type_instance,relating_type=wall_type_obj)
        ifcopenshell.api.run("geometry.edit_object_placement", self.file, product=ifc_wall_type_instance,matrix=matrix_1)
        ifcopenshell.api.run("spatial.assign_container", self.file, relating_structure=building_storey_obj,product=ifc_wall_type_instance)
        ifcopenshell.api.run("geometry.assign_representation", self.file, product=ifc_wall_type_instance,representation=representation)

    def place_slab(self, building_storey_obj, slab_type_obj, length, width, thickness, x, y, model_body, floor_name, floor_description):
        x = float(x)
        y = float(y)
        z = 0.0
        ifc_slab = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcSlab",
                                        name=floor_name)
        #ifc_slabtype = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcSlabType")
        ifc_slabtype = slab_type_obj
        ifcopenshell.api.run("type.assign_type", self.file, related_object=ifc_slab, relating_type=ifc_slabtype)

        pnt1 = self.file.createIfcCartesianPoint((x, y, z))
        pnt2 = self.file.createIfcCartesianPoint((x, y + length, z))
        pnt3 = self.file.createIfcCartesianPoint((x + width, y + length, z))
        pnt4 = self.file.createIfcCartesianPoint((x + width, y, z))

        slab_line = self.file.createIfcPolyline([pnt1, pnt2, pnt3, pnt4])
        ifcclosedprofile = self.file.createIfcArbitraryClosedProfileDef("AREA", None, slab_line)
        ifc_direction = self.file.createIfcDirection(Z)

        point = self.file.createIfcCartesianPoint((x, y, z))
        dir1 = self.file.createIfcDirection((0., 0., 1.))
        dir2 = self.file.createIfcDirection((1., 0., 0.))
        axis2placement = self.file.createIfcAxis2Placement3D(point, dir1, dir2)
        extrusion = thickness
        slab_solid = self.file.createIfcExtrudedAreaSolid(ifcclosedprofile, axis2placement, ifc_direction,
                                                          extrusion)
        shape_representation = self.file.createIfcShapeRepresentation(ContextOfItems=model_body,
                                                                      RepresentationIdentifier='Body',
                                                                      RepresentationType='SweptSolid',
                                                                      Items=[slab_solid])

        ifcopenshell.api.run("geometry.assign_representation", self.file, product=ifc_slabtype,
                             representation=shape_representation)
        ifcopenshell.api.run("spatial.assign_container", self.file, product=ifc_slab,
                             relating_structure=building_storey_obj)

    def place_column(self, building_storey_obj, column_type_obj, profile_type_obj, x, y, z, model_body, column_name, length):
        ifc_column_type_instance = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcColumn",name=column_name + "_instance")
        ifcopenshell.api.run("type.assign_type", self.file, related_object=ifc_column_type_instance, relating_type=column_type_obj)

        matrix_1 = numpy.array(
            (
                (1.0, 0.0, 0.0, x),
                (0.0, 1.0, 0.0, y),
                (0.0, 0.0, 1.0, z),
                (0.0, 0.0, 0.0, 1.0),
            )
        )
        representation = ifcopenshell.api.run("geometry.add_profile_representation", self.file, context=model_body, profile=profile_type_obj, depth=length)
        ifcopenshell.api.run("geometry.edit_object_placement",self.file, product=ifc_column_type_instance, matrix=matrix_1)
        ifcopenshell.api.run("spatial.assign_container", self.file, relating_structure=building_storey_obj, product=ifc_column_type_instance)
        ifcopenshell.api.run("geometry.assign_representation", self.file, product=ifc_column_type_instance, representation=representation)

    def place_beam(self, building_storey_obj, beam_type_obj, profile_type_obj, x, y, z, model_body, beam_name, length):
        ifc_beam_type_instance = ifcopenshell.api.run("root.create_entity", self.file, ifc_class="IfcBeam",name=beam_name + "_instance")
        ifcopenshell.api.run("type.assign_type", self.file, related_object=ifc_beam_type_instance, relating_type=beam_type_obj)

        matrix_1 = numpy.array(
            (
                (0.0, 0.0, 1.0, x),
                (0.0, 1.0, 0.0, y),
                (1.0, 0.0, 0.0, z),
                (0.0, 0.0, 0.0, 1.0),
            )
        )
        representation = ifcopenshell.api.run("geometry.add_profile_representation", self.file, context=model_body, profile=profile_type_obj, depth=length)
        ifcopenshell.api.run("geometry.edit_object_placement",self.file, product=ifc_beam_type_instance, matrix=matrix_1)
        ifcopenshell.api.run("spatial.assign_container", self.file, relating_structure=building_storey_obj, product=ifc_beam_type_instance)
        ifcopenshell.api.run("geometry.assign_representation", self.file, product=ifc_beam_type_instance, representation=representation)

    def load_ifc_automatically(self):
        if (bool(self.file)) == True:
            project = self.file.by_type('IfcProject')

            if project is not None:
                for i in project:
                    collection_name = 'IfcProject/' + i.Name

                collection = bpy.data.collections.get(str(collection_name))

                if collection is not None:
                    for obj in collection.objects:
                        bpy.data.objects.remove(obj, do_unlink=True)

                    bpy.data.collections.remove(collection)

            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
            bpy.ops.bim.load_project(filepath=library_path)

    def add_drawing(self):
        drawing.add_drawing(self.file, "collector", "test",  "PLAN_VIEW", "test")

    def create_ifcaxis2placement(self, point=O, dir1=Z, dir2=X):
        point = self.file.createIfcCartesianPoint(point)
        dir1 = self.file.createIfcDirection(dir1)
        dir2 = self.file.createIfcDirection(dir2)
        axis2placement = self.file.createIfcAxis2Placement3D(point, dir1, dir2)
        return axis2placement

    def create_ifclocalplacement(self, point=O, dir1=Z, dir2=X, relative_to=None):
        axis2placement = self.create_ifcaxis2placement(point, dir1, dir2)
        ifclocalplacement = self.file.createIfcLocalPlacement(relative_to, axis2placement)
        return ifclocalplacement

    def create_building_storeys(self, building_storeys):
        building_storeys_obj = []
        for i in building_storeys:
            name = i[0]
            elevation = i[1]
            building_storey_obj = self.file.createIfcBuildingStorey(create_guid(),
                                                              self.owner_history,
                                                              name,
                                                              None,
                                                              None,
                                                              self.storey_placement,
                                                              None,
                                                              None,
                                                              "ELEMENT",
                                                              float(elevation))

            container_storey = self.file.createIfcRelAggregates(create_guid(), self.owner_history, "Building Container", None, self.building, [building_storey_obj])
            building_storeys_obj.append(building_storey_obj)
        return building_storeys_obj

    def create_grid(self, grids_x_distance_between, grids_y_distance_between, grids_x_direction_amount,grids_y_direction_amount, grid_extends):

        grids_x_dictionary = OrderedDict()
        grids_y_dictionary = OrderedDict()

        x = -float(grids_x_distance_between)
        y = -float(grids_y_distance_between)

        for x_grids in range(0, int(grids_x_direction_amount), 1):
            x += float(grids_x_distance_between)
            grids_x_dictionary[x_grids] = x

        for y_grids in range(0, int(grids_y_direction_amount), 1):
            y += grids_y_distance_between
            grids_y_dictionary[y_grids] = y

        x_min = list(grids_x_dictionary.items())[0][1]
        x_max = list(grids_x_dictionary.items())[-1][1]

        y_min = list(grids_y_dictionary.items())[0][1]
        y_max = list(grids_y_dictionary.items())[-1][1]

        x_min_overlap = x_min - grid_extends
        x_max_overlap = x_max + grid_extends

        y_min_overlap = y_min - grid_extends
        y_max_overlap = y_max + grid_extends

        polylineSet = []
        gridX = []
        gridY = []

        for i_grid in grids_x_dictionary.items():
            point_1 = self.file.createIfcCartesianPoint((i_grid[1], y_min_overlap))
            point_2 = self.file.createIfcCartesianPoint((i_grid[1], y_max_overlap))

            Line = self.file.createIfcPolyline([point_1, point_2])
            polylineSet.append(Line)

            grid = self.file.createIfcGridAxis()
            grid.AxisTag = str(i_grid[0]) + "X"
            grid.AxisCurve = Line
            grid.SameSense = True
            gridX.append(grid)

        for i_grid in grids_y_dictionary.items():
            point_1 = self.file.createIfcCartesianPoint((x_min_overlap, i_grid[1]))
            point_2 = self.file.createIfcCartesianPoint((x_max_overlap, i_grid[1]))

            Line = self.file.createIfcPolyline([point_1, point_2])
            polylineSet.append(Line)

            grid = self.file.createIfcGridAxis()
            grid.AxisTag = str(i_grid[0]) + "Y"
            grid.AxisCurve = Line
            grid.SameSense = True
            gridY.append(grid)

        # Defining the grid
        PntGrid = self.file.createIfcCartesianPoint(O)

        myGridCoordinateSystem = self.file.createIfcAxis2Placement3D()
        myGridCoordinateSystem.Location = PntGrid
        myGridCoordinateSystem.Axis = self.axis_Z
        myGridCoordinateSystem.RefDirection = self.axis_X

        grid_placement = self.file.createIfcLocalPlacement()
        grid_placement.PlacementRelTo = self.storey_placement
        grid_placement.RelativePlacement = myGridCoordinateSystem

        grid_curvedSet = self.file.createIfcGeometricCurveSet(polylineSet)

        gridShape_Reppresentation = self.file.createIfcShapeRepresentation()
        gridShape_Reppresentation.ContextOfItems = self.footprint_context
        gridShape_Reppresentation.RepresentationIdentifier = 'FootPrint'
        gridShape_Reppresentation.RepresentationType = 'GeometricCurveSet'
        gridShape_Reppresentation.Items = [grid_curvedSet]

        grid_Representation = self.file.createIfcProductDefinitionShape()
        grid_Representation.Representations = [gridShape_Reppresentation]

        myGrid = self.file.createIfcGrid(create_guid(), self.owner_history)
        myGrid.ObjectPlacement = grid_placement
        myGrid.Representation = grid_Representation
        myGrid.UAxes = gridX
        myGrid.VAxes = gridY

        container_SpatialStructure = self.file.createIfcRelContainedInSpatialStructure(create_guid(), self.owner_history)
        container_SpatialStructure.Name = 'BuildingStoreyContainer'
        container_SpatialStructure.Description = 'BuildingStoreyContainer for Elements'
        container_SpatialStructure.RelatingStructure = self.site
        container_SpatialStructure.RelatedElements = [myGrid]

LibraryGenerator().generate()
