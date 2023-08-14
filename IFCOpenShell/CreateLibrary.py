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

import bpy
import ifcopenshell
import ifcopenshell.api
import blenderbim.tool as tool


class LibraryGenerator:
    def generate(self):
        ifcopenshell.api.pre_listeners = {}
        ifcopenshell.api.post_listeners = {}

        self.file = ifcopenshell.api.run("project.create_file")
        self.project = ifcopenshell.api.run(
            "root.create_entity", self.file, ifc_class="IfcProject", name="BlenderBIM NL ProjectTemplate 0.1"
        )
        self.library = ifcopenshell.api.run(
            "root.create_entity", self.file, ifc_class="IfcProjectLibrary", name="BlenderBIM NL Library 0.1"
        )
        ifcopenshell.api.run(
            "project.assign_declaration", self.file, definition=self.library, relating_context=self.project
        )
        ifcopenshell.api.run("unit.assign_unit", self.file,
                             length={"is_metric": True, "raw": "MILLIMETERS"})  # METERS OR MILLIMETERS
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
        # 0 MATERIALS

        # 0.1 MATERIAL PROFILE SETS

        # materialcategories
        steel = "steel"
        metal = "metal"
        concrete = "concrete"
        timber = "wood"
        masonry = "masonry"
        ceramic = "ceramic"
        other = "other"

        # materials name / category /
        material_names = [
            ["onbekend", other],
            ["beton", concrete],
            ["staal", steel],
            ["staal_S235", steel],
            ["staal_S275", steel],
            ["staal_S355", steel],
            ["staal_S235JR2", steel],
            ["staal_4.6", steel],
            ["staal_8.8", steel],
            ["staal_10.9", steel],
            ["staal_RVS", steel],
            ["staal_gietijzer", steel],
            ["betonstaal", steel],
            ["betonstaal_FeB220", steel],
            ["betonstaal_FeB400", steel],
            ["betonstaal_FeB500", steel],
            ["betonstaal_B500", steel],
            ["metaal", metal],
            ["zink", metal],
            ["lood", metal],
            ["koper", metal],
            ["hout", timber],
            ["hout_naald", timber],
            ["hout_loof", timber],
            ["hout_vuren", timber],
            ["hout_eiken", timber],
            ["hout_merbau", timber],
            ["hout_meranti", timber],
            ["hout_jatoba", timber],
            ["hout_mahonie", timber],
            ["hout_azobe", timber],
            ["beton_prefab", concrete],
            ["beton_tpg", concrete],
            ["beton_C20/25", concrete],
            ["beton_C25/35", concrete],
            ["beton_C35/45", concrete],
            ["keramiek", ceramic],
            ["metselwerk", masonry],
            ["metselwerk_waalformaat", masonry],
            ["riet", other]
        ]

        for material_name in material_names:
            ifcopenshell.api.run("material.add_material", self.file, name=material_name[0], category=material_name[1])

        self.material = ifcopenshell.api.run("material.add_material", self.file, name="Unknown")

        # 1 WALL TYPES
        walltypes = [
            ["gen_100", 100],
            ["gen_200", 200],
            ["gen_300", 300],
            ["ls_70", 70],
            ["mw_100", 100],
            ["mw_210", 210],
            ["isolatie_100", 100],
            ["isolatie_pir_100", 100],
            ["isolatie_pir_110", 110],
            ["isolatie_pur_100", 100],
            ["kzst_100", 100],
            ["kzst_120", 120],
            ["kzst_150", 150],
            ["kzst_214", 214],
            ["mplex_10", 10],
            ["mplex_12", 12],
            ["mplex_15", 15],
            ["mplex_18", 18],
            ["prefab_beton_100", 100],
            ["prefab_beton_180", 180],
            ["prefab_beton_250", 250],
            ["beton_250", 250],
            ["clt_70", 70],
            ["clt_90", 90],
            ["clt_100", 100],
            ["clt_120", 120],
            ["clt_140", 140],
            ["clt_160", 160],
            ["clt_200", 200],
            ["clt_220", 220]
        ]

        for walltype in walltypes:
            self.create_layer_type("IfcWallType", walltype[0], walltype[1])

        # 2 FLOOR TYPES
        floortypes = [
            ["gen_100", 100],
            ["gen_200", 200],
            ["gen_300", 300],
            ["isolatie_100", 100],
            ["isolatie_pir_100", 100],
            ["isolatie_pir_110", 110],
            ["isolatie_pur_100", 100],
            ["isolatie_eps_100", 100],
            ["mplex_18", 18],
            ["kpv_150", 150],
            ["kpv_200", 200],
            ["kpv_260", 260],
            ["kpv_320", 320],
            ["kpv_400", 400],
            ["prefab_beton_200", 200],
            ["prefab_beton_250", 250],
            ["beton_100", 100],
            ["beton_150", 150],
            ["beton_200", 200],
            ["beton_250", 250],
            ["clt_70", 70],
            ["clt_90", 90],
            ["clt_100", 100],
            ["clt_120", 120],
            ["clt_140", 140],
            ["clt_160", 160],
            ["clt_200", 200],
            ["clt_220", 220]
        ]

        for floortype in floortypes:
            self.create_layer_type("IfcSlabType", floortype[0], floortype[1])

        self.create_layer_type("IfcCoveringType", "COV10", 10)

        product = self.create_layer_type("IfcCoveringType", "COV20", 20)
        pset = ifcopenshell.api.run("pset.add_pset", self.file, product=product, name="EPset_Parametric")
        ifcopenshell.api.run("pset.edit_pset", self.file, pset=pset, properties={"LayerSetDirection": "AXIS2"})

        product = self.create_layer_type("IfcCoveringType", "COV30", 30)
        pset = ifcopenshell.api.run("pset.add_pset", self.file, product=product, name="EPset_Parametric")
        ifcopenshell.api.run("pset.edit_pset", self.file, pset=pset, properties={"LayerSetDirection": "AXIS3"})

        self.create_layer_type("IfcRampType", "RAM200", 20)

        # profile = self.file.create_entity("IfcCircleProfileDef", ProfileType="AREA", Radius=0.3)
        # self.create_profile_type("IfcPileType", "P1", profile)

        # 3 WOOD PROFILES, BEAMS
        woodprofiles = [
            ["HB 22x100", 22, 100],
            ["HB 28x245", 28, 245],
            ["HB 44x44", 44, 44],
            ["HB 44x70", 44, 70],
            ["HB 44x96", 44, 96],
            ["HB 44x121", 44, 121],
            ["HB 46x146", 46, 146],
            ["HB 46x171", 46, 171],
            ["HB 71x146", 71, 146],
            ["HB 71x171", 71, 171],
            ["HB 71x196", 71, 196],
            ["HB 71x221", 71, 221],
            ["HB 96x96", 96, 96],
            ["HB 96x171", 96, 171],
            ["HB 96x196", 96, 196],
            ["HB 96x221", 96, 221],
            ["SLS 38x38", 38, 38],
            ["SLS 38x89", 38, 89],
            ["SLS 38x121", 38, 121],
            ["SLS 38x140", 38, 38],
            ["SLS 38x156", 38, 156],
            ["SLS 38x184", 38, 184],
            ["SLS 38x235", 38, 235],
            ["SLS 38x286", 38, 286]
        ]

        for woodprofile in woodprofiles:
            profile = self.file.create_entity(
                "IfcRectangleProfileDef", ProfileName=woodprofile[0], ProfileType="AREA", XDim=woodprofile[1],
                YDim=woodprofile[2]
            )
            self.create_profile_type("IfcBeamType", woodprofile[0], profile)

        # 4 CONCRETE PROFILES, BEAMS
        concrete_rectangle_profiles = [
            ["BB 300x300", 300, 300],
            ["BB 300x400", 300, 400],
            ["BB 350x400", 350, 400],
            ["BB 350x450", 350, 450],
            ["BB 350x500", 350, 500],
            ["BB 400x500", 400, 500],
            ["BB 400x600", 400, 600],
            ["BB 500x600", 500, 600],
            ["BB 500x700", 500, 700]
        ]

        for concrete_rectangle_profile in concrete_rectangle_profiles:
            profile = self.file.create_entity(
                "IfcRectangleProfileDef", ProfileName=concrete_rectangle_profile[0], ProfileType="AREA",
                XDim=concrete_rectangle_profile[1], YDim=concrete_rectangle_profile[2]
            )
            self.create_profile_type("IfcBeamType", concrete_rectangle_profile[0], profile)

        # 5 CONCRETE PROFILES, COLUMNS
        concrete_rectangle_profiles = [
            ["BK 300x300", 300, 300],
            ["BK 350x350", 350, 350],
            ["BK 400x400", 400, 400],
            ["Opstort 400x400", 400, 400],
            ["BK 450x450", 450, 450],
            ["BK 500x500", 500, 500]
        ]

        for concrete_rectangle_profile in concrete_rectangle_profiles:
            profile = self.file.create_entity(
                "IfcRectangleProfileDef", ProfileName=concrete_rectangle_profile[0], ProfileType="AREA",
                XDim=concrete_rectangle_profile[1], YDim=concrete_rectangle_profile[2]
            )
            # self.create_profile_type("IfcColumnType", concrete_rectangle_profiles[0], profile)

        # 6 GENRIC PROFILES, COLUMNS

        generic_round_profiles = [
            ["GEN R150", 75],
            ["GEN R200", 100],
            ["GEN R250", 125],
            ["GEN R300", 150],
            ["GEN R500", 250]
        ]

        for generic_round_profile in generic_round_profiles:
            profile = self.file.create_entity(
                "IfcCircleProfileDef", ProfileName=generic_round_profile[0], ProfileType="AREA",
                Radius=generic_round_profile[1]
            )
            self.create_profile_type("IfcColumnType", generic_round_profile[0], profile)

        # 6 GENRIC PROFILES, COLUMNS, BEAMS
        generic_rectangle_profiles = [
            ["GEN 100x100", 100, 100],
            ["GEN 150x150", 150, 150],
            ["GEN 200x200", 200, 200],
            ["GEN 250x250", 250, 250],
            ["GEN 300x300", 300, 300],
            ["GEN 350x350", 350, 350],
            ["GEN 400x400", 400, 400]
        ]

        for generic_rectangle_profile in generic_rectangle_profiles:
            profile = self.file.create_entity(
                "IfcRectangleProfileDef", ProfileName=generic_rectangle_profile[0], ProfileType="AREA",
                XDim=generic_rectangle_profile[1], YDim=generic_rectangle_profile[2]
            )
            self.create_profile_type("IfcBeamType", generic_rectangle_profile[0], profile)
            self.create_profile_type("IfcColumnType", generic_rectangle_profile[0], profile)

        # steelprofiles =

        self.create_line_type("DASHED", "dashed")
        self.create_line_type("FINE", "fine")
        self.create_line_type("THIN", "thin")
        self.create_line_type("MEDIUM", "medium")
        self.create_line_type("THICK", "thick")
        self.create_line_type("STRONG", "strong")
        self.create_text_type("DOOR-TAG", "door-tag", ["{{type.Name}}", "{{Name}}"])
        self.create_text_type("WINDOW-TAG", "window-tag", ["{{Name}}"])
        self.create_text_type("SPACE-TAG", "space-tag", ["{{Name}}", "{{Description}}",
                                                         "``round({{Qto_SpaceBaseQuantities.NetFloorArea}} or 0., 2)``"])
        self.create_text_type("MATERIAL-TAG", "rectangle-tag", ["{{material.Name}}"])
        self.create_text_type("TYPE-TAG", "capsule-tag", ["{{type.Name}}"])
        self.create_text_type("NAME-TAG", "capsule-tag", ["{{Name}}"])

        self.file.write("C:/BlenderBIM/3bm/Standards test folder/IFC4 NL Demo Template 0.1.ifc")

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

    def create_layer_type(self, ifc_class, name, thickness):
        element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class=ifc_class, name=name)
        rel = ifcopenshell.api.run("material.assign_material", self.file, product=element, type="IfcMaterialLayerSet")
        layer_set = rel.RelatingMaterial
        layer = ifcopenshell.api.run("material.add_layer", self.file, layer_set=layer_set, material=self.material)
        layer.LayerThickness = thickness
        ifcopenshell.api.run("project.assign_declaration", self.file, definition=element, relating_context=self.library)
        return element

    def create_profile_type(self, ifc_class, name, profile):
        element = ifcopenshell.api.run("root.create_entity", self.file, ifc_class=ifc_class, name=name)
        rel = ifcopenshell.api.run("material.assign_material", self.file, product=element, type="IfcMaterialProfileSet")
        profile_set = rel.RelatingMaterial
        material_profile = ifcopenshell.api.run(
            "material.add_profile", self.file, profile_set=profile_set, material=self.material
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


LibraryGenerator().generate()
