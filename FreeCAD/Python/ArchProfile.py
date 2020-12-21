#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2011                                                    *
#*   Yorik van Havre <yorik@uncreated.net>                                 *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

__title__= "FreeCAD Profile"
__author__ = "Yorik van Havre"
# Extended by Maarten Vroegindeweij

__url__ = "http://www.freecadweb.org"

## @package ArchProfile
#  \ingroup ARCH
#  \brief Profile tools for ArchStructure
#
#  This module provides tools to build base profiles
#  for Arch Structure elements


import FreeCAD, Draft, os
from FreeCAD import Vector
import csv

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
    from PySide.QtCore import QT_TRANSLATE_NOOP
else:
    # \cond
    def translate(ctxt,txt):
        return txt
    def QT_TRANSLATE_NOOP(ctxt,txt):
        return txt
    # \endcond


# Presets in the form: Class, Name, Profile type, [profile data]
# Search for profiles.csv in data/Mod/Arch/Presets and in the same folder as this file
profilefiles = [os.path.join(FreeCAD.getResourceDir(),"Mod","Arch","Presets","profiles.csv"),
                os.path.join(os.path.dirname(__file__),"Presets","profiles.csv")]

def makewire(path,checkclosed=False,donttry=False):
		'''try to make a wire out of the list of edges. If the 'Wire' functions fails or the wire is not
		closed if required the 'connectEdgesToWires' function is used'''
		if not donttry:
				try:
						import Part
						sh = Part.Wire(Part.__sortEdges__(path))
						#sh = Part.Wire(path)
						isok = (not checkclosed) or sh.isClosed()
				except Part.OCCError:# BRep_API:command not done
						isok = False
		if donttry or not isok:
						#Code from wmayer forum p15549 to fix the tolerance problem
						#original tolerance = 0.00001
						comp=Part.Compound(path)
						sh = comp.connectEdgesToWires(False,10**(-1*(Draft.precision()-2))).Wires[0]
		return sh 



def readPresets():

    Presets=[]
    for profilefile in profilefiles:
        if os.path.exists(profilefile):
            try:
                with open(profilefile, "r") as csvfile:
                    beamreader = csv.reader(csvfile)
                    bid=1 #Unique index
                    for row in beamreader:
                        if (not row) or row[0].startswith("#"):
                            continue
                        try:
                            r=[bid, row[0], row[1], row[2]]
                            for i in range(3,len(row)):
                                r=r+[float(row[i])]
                            if not r in Presets:
                                Presets.append(r)
                            bid=bid+1
                        except ValueError:
                            print("Skipping bad line: "+str(row))
            except IOError:
                print("Could not open ",profilefile)
    return Presets

def makeProfile(profile=[0,'REC','REC100x100','R',100,100]):

    '''makeProfile(profile): returns a shape  with the face defined by the profile data'''

    if not FreeCAD.ActiveDocument:
        FreeCAD.Console.PrintError("No active document. Aborting\n")
        return
    obj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython",profile[2])
    obj.Label = profile[2]

    if profile[3]=="Generic_RCT":
        _Profile_Generic_RCT(obj, profile)
    elif profile[3] =="SteelCF_C":
        _Profile_SteelCF_C(obj,profile)
    elif profile[3] =="SteelCF_C_WL":
        _Profile_SteelCF_C_WL(obj,profile)
    elif profile[3] =="SteelCF_L":
        _Profile_SteelCF_L(obj,profile)
    elif profile[3] =="SteelCF_Sigma_WL":
        _Profile_SteelCF_Sigma_WL(obj,profile)
    elif profile[3] =="SteelCF_Z":
        _Profile_SteelCF_Z(obj,profile)
    elif profile[3] =="SteelCF_Z_WL":
        _Profile_SteelCF_Z_WL(obj,profile)
    elif profile[3]=="SteelHR_CHS":
        _Profile_SteelHR_CHS(obj, profile)
    elif profile[3]=="SteelHR_I_PF":
        _Profile_SteelHR_I_PF(obj, profile)
    elif profile[3]=="SteelHR_I_SF":
        _Profile_SteelHR_I_SF(obj, profile)
    elif profile[3]=="SteelHR_L":
        _Profile_SteelHR_L(obj, profile)
    elif profile[3]=="SteelHR_RS":
        _Profile_SteelHR_RS(obj, profile)
    elif profile[3]=="SteelHR_RHS":
        _Profile_SteelHR_RHS(obj, profile)
    elif profile[3]=="SteelHR_RCT":
        _Profile_SteelHR_RCT(obj, profile)
    elif profile[3]== "SteelHR_R":
        _Profile_SteelHR_Round(obj, profile)
    elif profile[3]=="SteelHR_C_PF":
        _Profile_SteelHR_C_PF(obj, profile)
    elif profile[3]=="SteelHR_C_SF":
        _Profile_SteelHR_C_SF(obj, profile)
    else :
        print("Profile not supported")
    if FreeCAD.GuiUp:
        ViewProviderProfile(obj.ViewObject)
    return obj


class _Profile(Draft._DraftObject):

    '''Superclass for Profile classes'''

    def __init__(self,obj, profile):
        self.Profile=profile
        Draft._DraftObject.__init__(self,obj,"Profile")

class _Profile_Generic_RCT(_Profile):

    '''A parametric rectangular beam profile based on [Width, Height]'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = obj.Width.Value/2
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        pl = obj.Placement
        p1 = Vector(-obj.Width.Value/2,-obj.Height.Value/2,0)
        p2 = Vector(obj.Width.Value/2,-obj.Height.Value/2,0)
        p3 = Vector(obj.Width.Value/2,obj.Height.Value/2,0)
        p4 = Vector(-obj.Width.Value/2,obj.Height.Value/2,0)
        p = Part.makePolygon([p1,p2,p3,p4,p1])
        p = Part.Face(p)
        #p.reverse()
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelCF_C(_Profile):

   '''Cold formed C-profile'''

   def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web and flange")).Thickness = profile[6]
        obj.addProperty("App::PropertyLength","InnerFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Inner fillet")).InnerFillet = profile[7]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = profile[8]
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        
        _Profile.__init__(self,obj,profile)

   def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        t = obj.Thickness.Value
        r1 = obj.InnerFillet.Value
        r11 = r1/math.sqrt(2)
        r2 = r1+t
        r21 = r2/math.sqrt(2)
        ex = obj.CentroidHorizontal.Value #from left
        ey = obj.CentroidVertical.Value #from bottom

        pl = obj.Placement
        p1 = [-ex,-ey+r2] #start arc left bottom
        p2 = [-ex+r2-r21,-ey+r2-r21] #second point arc
        p3 = [-ex+r2,-ey] #end arc
        p4 = [b-ex,-ey] #right bottom
        p5 = [b-ex,-ey+t]
        p6 = [-ex+t+r1,-ey+t] #start arc
        p7 = [-ex+t+r1-r11,-ey+t+r1-r11] #second point arc
        p8 = [-ex+t,-ey+t+r1] #end arc
        p9 = [p8[0],-p8[1]]
        p10 = [p7[0],-p7[1]]
        p11 = [p6[0],-p6[1]]
        p12 = [p5[0],-p5[1]]
        p13 = [p4[0],-p4[1]]
        p14 = [p3[0],-p3[1]]
        p15 = [p2[0],-p2[1]]
        p16 = [p1[0],-p1[1]]

        l1 = Part.Arc(Vector(p1[0],p1[1],0),Vector(p2[0],p2[1],0),Vector(p3[0],p3[1],0))
        l1 = l1.toShape()
        l2 = Part.makeLine(Vector((p3[0]),p3[1],0),Vector(p4[0],p4[1],0))
        l3 = Part.makeLine(Vector((p4[0]),p4[1],0),Vector(p5[0],p5[1],0))
        l4 = Part.makeLine(Vector((p5[0]),p5[1],0),Vector(p6[0],p6[1],0))
        l5 = Part.Arc(Vector(p6[0],p6[1],0),Vector(p7[0],p7[1],0),Vector(p8[0],p8[1],0))
        l5 = l5.toShape()
        l6 = Part.makeLine(Vector((p8[0]),p8[1],0),Vector(p9[0],p9[1],0))
        l7 = Part.Arc(Vector(p9[0],p9[1],0),Vector(p10[0],p10[1],0),Vector(p11[0],p11[1],0))
        l7 = l7.toShape()
        l8 = Part.makeLine(Vector((p11[0]),p11[1],0),Vector(p12[0],p12[1],0))
        l9 = Part.makeLine(Vector((p12[0]),p12[1],0),Vector(p13[0],p13[1],0))
        l10 = Part.makeLine(Vector((p13[0]),p13[1],0),Vector(p14[0],p14[1],0))
        l11 = Part.Arc(Vector(p14[0],p14[1],0),Vector(p15[0],p15[1],0),Vector(p16[0],p16[1],0))
        l11 = l11.toShape()
        l12 = Part.makeLine(Vector((p16[0]),p16[1],0),Vector(p1[0],p1[1],0))

        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12])
        
        p = Part.Face(aWire)
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelCF_C_WL(_Profile):

   '''Cold formed C-profile with lips'''
   def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web and flange")).Thickness = profile[6]
        obj.addProperty("App::PropertyLength","InnerFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Inner fillet")).InnerFillet = profile[7]
        obj.addProperty("App::PropertyLength","LipLength","Draft",QT_TRANSLATE_NOOP("App::Property","Length of lip")).LipLength = profile[8]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = profile[9]
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        
        _Profile.__init__(self,obj,profile)

   def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        t = obj.Thickness.Value
        h1 = obj.LipLength.Value
        r1 = obj.InnerFillet.Value
        r11 = r1/math.sqrt(2)
        r2 = r1+t
        r21 = r2/math.sqrt(2)
        ex = obj.CentroidHorizontal.Value #from left
        ey = obj.CentroidVertical.Value #from bottom

        pl = obj.Placement
        p1 = [-ex,-ey+r2] #start arc left bottom
        p2 = [-ex+r2-r21,-ey+r2-r21] #second point arc
        p3 = [-ex+r2,-ey] #end arc
        p4 = [b-ex-r2,-ey] #start arc
        p5 = [b-ex-r2+r21,-ey+r2-r21] #second point arc
        p6 = [b-ex,-ey+r2] #end arc
        p7 = [b-ex,-ey+h1] #end lip
        p8 = [b-ex-t,-ey+h1] 
        p9 = [b-ex-t,-ey+t+r1] #start arc
        p10 = [b-ex-t-r1+r11,-ey+t+r1-r11] #second point arc
        p11 = [b-ex-t-r1,-ey+t] #end arc
        p12 = [-ex+t+r1,-ey+t] #start arc
        p13 = [-ex+t+r1-r11,-ey+t+r1-r11] #second point arc
        p14 = [-ex+t,-ey+t+r1] #end arc
        p15 = [p14[0],-p14[1]]
        p16 = [p13[0],-p13[1]]
        p17 = [p12[0],-p12[1]]
        p18 = [p11[0],-p11[1]]
        p19 = [p10[0],-p10[1]]
        p20 = [p9[0],-p9[1]]
        p21 = [p8[0],-p8[1]]
        p22 = [p7[0],-p7[1]]
        p23 = [p6[0],-p6[1]]
        p24 = [p5[0],-p5[1]]
        p25 = [p4[0],-p4[1]]
        p26 = [p3[0],-p3[1]]
        p27 = [p2[0],-p2[1]]
        p28 = [p1[0],-p1[1]]

        l1 = Part.Arc(Vector(p1[0],p1[1],0),Vector(p2[0],p2[1],0),Vector(p3[0],p3[1],0))
        l1 = l1.toShape()
        l2 = Part.makeLine(Vector((p3[0]),p3[1],0),Vector(p4[0],p4[1],0))
        l3 = Part.Arc(Vector(p4[0],p4[1],0),Vector(p5[0],p5[1],0),Vector(p6[0],p6[1],0))
        l3 = l3.toShape()
        l4 = Part.makeLine(Vector((p6[0]),p6[1],0),Vector(p7[0],p7[1],0))
        l5 = Part.makeLine(Vector((p7[0]),p7[1],0),Vector(p8[0],p8[1],0))
        l6 = Part.makeLine(Vector((p8[0]),p8[1],0),Vector(p9[0],p9[1],0))
        l7 = Part.Arc(Vector(p9[0],p9[1],0),Vector(p10[0],p10[1],0),Vector(p11[0],p11[1],0))
        l7 = l7.toShape()
        l8 = Part.makeLine(Vector((p11[0]),p11[1],0),Vector(p12[0],p12[1],0))
        l9 = Part.Arc(Vector(p12[0],p12[1],0),Vector(p13[0],p13[1],0),Vector(p14[0],p14[1],0))
        l9 = l9.toShape()        
        l10 = Part.makeLine(Vector((p14[0]),p14[1],0),Vector(p15[0],p15[1],0))
        l11 = Part.Arc(Vector(p15[0],p15[1],0),Vector(p16[0],p16[1],0),Vector(p17[0],p17[1],0))
        l11 = l11.toShape() 
        l12 = Part.makeLine(Vector((p17[0]),p17[1],0),Vector(p18[0],p18[1],0))
        l13 = Part.Arc(Vector(p18[0],p18[1],0),Vector(p19[0],p19[1],0),Vector(p20[0],p20[1],0))
        l13 = l13.toShape() 
        l14 = Part.makeLine(Vector((p20[0]),p20[1],0),Vector(p21[0],p21[1],0))
        l15 = Part.makeLine(Vector((p21[0]),p21[1],0),Vector(p22[0],p22[1],0))
        l16 = Part.makeLine(Vector((p22[0]),p22[1],0),Vector(p23[0],p23[1],0))
        l17 = Part.Arc(Vector(p23[0],p23[1],0),Vector(p24[0],p24[1],0),Vector(p25[0],p25[1],0))
        l17 = l17.toShape() 
        l18 = Part.makeLine(Vector((p25[0]),p25[1],0),Vector(p26[0],p26[1],0))
        l19 = Part.Arc(Vector(p26[0],p26[1],0),Vector(p27[0],p27[1],0),Vector(p28[0],p28[1],0))
        l19 = l19.toShape() 
        l20 = Part.makeLine(Vector((p28[0]),p28[1],0),Vector(p1[0],p1[1],0))

        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17,l18,l19,l20])
        
        p = Part.Face(aWire)
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelCF_L(_Profile):

   '''Cold formed L-profile'''

   def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web and flange")).Thickness = profile[6]
        obj.addProperty("App::PropertyLength","InnerFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Inner fillet")).InnerFillet = profile[7]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = profile[8]
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        
        _Profile.__init__(self,obj,profile)

   def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        t = obj.Thickness.Value
        r1 = obj.InnerFillet.Value
        r11 = r1/math.sqrt(2)
        r2 = r1+t
        r21 = r2/math.sqrt(2)
        ex = obj.CentroidHorizontal.Value #from left
        ey = obj.CentroidVertical.Value #from bottom

        pl = obj.Placement
        p1 = [-ex,-ey+r2] #start arc left bottom
        p2 = [-ex+r2-r21,-ey+r2-r21] #second point arc
        p3 = [-ex+r2,-ey] #end arc
        p4 = [b-ex,-ey] #right bottom
        p5 = [b-ex,-ey+t]
        p6 = [-ex+t+r1,-ey+t] #start arc
        p7 = [-ex+t+r1-r11,-ey+t+r1-r11] #second point arc
        p8 = [-ex+t,-ey+t+r1] #end arc
        p9 = [-ex+t,ey]
        p10 = [-ex,ey] #left top

        l1 = Part.Arc(Vector(p1[0],p1[1],0),Vector(p2[0],p2[1],0),Vector(p3[0],p3[1],0))
        l1 = l1.toShape()
        l2 = Part.makeLine(Vector((p3[0]),p3[1],0),Vector(p4[0],p4[1],0))
        l3 = Part.makeLine(Vector((p4[0]),p4[1],0),Vector(p5[0],p5[1],0))
        l4 = Part.makeLine(Vector((p5[0]),p5[1],0),Vector(p6[0],p6[1],0))
        l5 = Part.Arc(Vector(p6[0],p6[1],0),Vector(p7[0],p7[1],0),Vector(p8[0],p8[1],0))
        l5 = l5.toShape()
        l6 = Part.makeLine(Vector((p8[0]),p8[1],0),Vector(p9[0],p9[1],0))
        l7 = Part.makeLine(Vector((p9[0]),p9[1],0),Vector(p10[0],p10[1],0))  
        l8 = Part.makeLine(Vector((p10[0]),p10[1],0),Vector(p1[0],p1[1],0))    
        
        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8])
        
        p = Part.Face(aWire)
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelCF_Sigma_WL(_Profile):

   '''Cold formed Sigma-profile with lips'''
   def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web and flange")).Thickness = profile[6]
        obj.addProperty("App::PropertyLength","InnerFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Inner fillet")).InnerFillet = profile[7]
        obj.addProperty("App::PropertyLength","LipLength","Draft",QT_TRANSLATE_NOOP("App::Property","Length of lip")).LipLength = profile[8]
        obj.addProperty("App::PropertyLength","MiddleBendLength","Draft",QT_TRANSLATE_NOOP("App::Property","Length of middle bend")).MiddleBendLength = profile[9]
        obj.addProperty("App::PropertyLength","TopBendLength","Draft",QT_TRANSLATE_NOOP("App::Property","Length of top bend")).TopBendLength = profile[10]
        obj.addProperty("App::PropertyLength","MiddleBendWidth","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the middle bend from the exterior face")).MiddleBendWidth = profile[11]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = profile[12]
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        
        _Profile.__init__(self,obj,profile)

   def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        b2 = obj.MiddleBendWidth.Value
        h = obj.Height.Value
        t = obj.Thickness.Value
        h1 = obj.LipLength.Value
        h2 = obj.MiddleBendLength.Value
        h3 = obj.TopBendLength.Value
        h4 = (h-h2-h3*2)/2
        h5 = math.tan(0.5*math.atan(b2/h4))*t
        r1 = obj.InnerFillet.Value
        r11 = r1/math.sqrt(2)
        r2 = r1+t
        r21 = r2/math.sqrt(2)
        ex = obj.CentroidHorizontal.Value #from left
        ey = obj.CentroidVertical.Value #from bottom

        pl = obj.Placement
        p1 = [-ex+b2,-h2/2]
        p2 = [-ex,-ey+h3]
        p3 = [-ex,-ey+r2] #start arc left bottom
        p4 = [-ex+r2-r21,-ey+r2-r21] #second point arc
        p5 = [-ex+r2,-ey] #end arc
        p6 = [b-ex-r2,-ey] #start arc
        p7 = [b-ex-r2+r21,-ey+r2-r21] #second point arc
        p8 = [b-ex,-ey+r2] #end arc
        p9 = [b-ex,-ey+h1] #end lip
        p10 = [b-ex-t,-ey+h1] 
        p11 = [b-ex-t,-ey+t+r1] #start arc
        p12 = [b-ex-t-r1+r11,-ey+t+r1-r11] #second point arc
        p13 = [b-ex-t-r1,-ey+t] #end arc
        p14 = [-ex+t+r1,-ey+t] #start arc
        p15 = [-ex+t+r1-r11,-ey+t+r1-r11] #second point arc
        p16 = [-ex+t,-ey+t+r1] #end arc
        p17 = [-ex+t,-ey+h3-h5]
        p18 = [-ex+b2+t,-h2/2-h5]
        p19 = [p18[0],-p18[1]]
        p20 = [p17[0],-p17[1]]
        p21 = [p16[0],-p16[1]]
        p22 = [p15[0],-p15[1]]
        p23 = [p14[0],-p14[1]]
        p24 = [p13[0],-p13[1]]
        p25 = [p12[0],-p12[1]]
        p26 = [p11[0],-p11[1]]
        p27 = [p10[0],-p10[1]]
        p28 = [p9[0],-p9[1]]
        p29 = [p8[0],-p8[1]]
        p30 = [p7[0],-p7[1]]
        p31 = [p6[0],-p6[1]]
        p32 = [p5[0],-p5[1]]
        p33 = [p4[0],-p4[1]]
        p34 = [p3[0],-p3[1]]
        p35 = [p2[0],-p2[1]]
        p36 = [p1[0],-p1[1]]

        l1 = Part.makeLine(Vector((p1[0]),p1[1],0),Vector(p2[0],p2[1],0))
        l2 = Part.makeLine(Vector((p2[0]),p2[1],0),Vector(p3[0],p3[1],0))
        l3 = Part.Arc(Vector(p3[0],p3[1],0),Vector(p4[0],p4[1],0),Vector(p5[0],p5[1],0))
        l3 = l3.toShape()
        l4 = Part.makeLine(Vector((p5[0]),p5[1],0),Vector(p6[0],p6[1],0))
        l5 = Part.Arc(Vector(p6[0],p6[1],0),Vector(p7[0],p7[1],0),Vector(p8[0],p8[1],0))
        l5 = l5.toShape()
        l6 = Part.makeLine(Vector((p8[0]),p8[1],0),Vector(p9[0],p9[1],0))
        l7 = Part.makeLine(Vector((p9[0]),p9[1],0),Vector(p10[0],p10[1],0))
        l8 = Part.makeLine(Vector((p10[0]),p10[1],0),Vector(p11[0],p11[1],0))
        l9 = Part.Arc(Vector(p11[0],p11[1],0),Vector(p12[0],p12[1],0),Vector(p13[0],p13[1],0))
        l9 = l9.toShape()
        l10 = Part.makeLine(Vector((p13[0]),p13[1],0),Vector(p14[0],p14[1],0))
        l11 = Part.Arc(Vector(p14[0],p14[1],0),Vector(p15[0],p15[1],0),Vector(p16[0],p16[1],0))
        l11 = l11.toShape()        
        l12 = Part.makeLine(Vector((p16[0]),p16[1],0),Vector(p17[0],p17[1],0))
        l13 = Part.makeLine(Vector((p17[0]),p17[1],0),Vector(p18[0],p18[1],0))
        l14 = Part.makeLine(Vector((p18[0]),p18[1],0),Vector(p19[0],p19[1],0))
        l15 = Part.makeLine(Vector((p19[0]),p19[1],0),Vector(p20[0],p20[1],0))
        l16 = Part.makeLine(Vector((p20[0]),p20[1],0),Vector(p21[0],p21[1],0))
        l17 = Part.Arc(Vector(p21[0],p21[1],0),Vector(p22[0],p22[1],0),Vector(p23[0],p23[1],0))
        l17 = l17.toShape() 
        l18 = Part.makeLine(Vector((p23[0]),p23[1],0),Vector(p24[0],p24[1],0))
        l19 = Part.Arc(Vector(p24[0],p24[1],0),Vector(p25[0],p25[1],0),Vector(p26[0],p26[1],0))
        l19 = l19.toShape() 
        l20 = Part.makeLine(Vector((p26[0]),p26[1],0),Vector(p27[0],p27[1],0))
        l21 = Part.makeLine(Vector((p27[0]),p27[1],0),Vector(p28[0],p28[1],0))
        l22 = Part.makeLine(Vector((p28[0]),p28[1],0),Vector(p29[0],p29[1],0))
        l23 = Part.Arc(Vector(p29[0],p29[1],0),Vector(p30[0],p30[1],0),Vector(p31[0],p31[1],0))
        l23 = l23.toShape() 
        l24 = Part.makeLine(Vector((p31[0]),p31[1],0),Vector(p32[0],p32[1],0))
        l25 = Part.Arc(Vector(p32[0],p32[1],0),Vector(p33[0],p33[1],0),Vector(p34[0],p34[1],0))
        l25 = l25.toShape() 
        l26 = Part.makeLine(Vector((p34[0]),p34[1],0),Vector(p35[0],p35[1],0))
        l27 = Part.makeLine(Vector((p35[0]),p35[1],0),Vector(p36[0],p36[1],0))
        l28 = Part.makeLine(Vector((p36[0]),p36[1],0),Vector(p1[0],p1[1],0))

 
        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17,l18,l19,l20,l21,l22,l23,l24,l25,l26,l27,l28])
        
        p = Part.Face(aWire)
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelCF_Z(_Profile):

   '''Cold formed Z-profile'''

   def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web and flange")).Thickness = profile[6]
        obj.addProperty("App::PropertyLength","InnerFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Inner fillet")).InnerFillet = profile[7]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = obj.Width/2
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        
        _Profile.__init__(self,obj,profile)

   def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        t = obj.Thickness.Value
        r1 = obj.InnerFillet.Value
        r11 = r1/math.sqrt(2)
        r2 = r1+t
        r21 = r2/math.sqrt(2)
        ex = obj.CentroidHorizontal.Value #from left
        ey = obj.CentroidVertical.Value #from bottom

        pl = obj.Placement
        p1 = [-0.5*t,-ey+t+r1] #start arc
        p2 = [-0.5*t-r1+r11,-ey+t+r1-r11] #second point arc
        p3 = [-0.5*t-r1,-ey+t] #end arc
        p4 = [-ex,-ey+t]
        p5 = [-ex,-ey] #left bottom
        p6 = [-r2+0.5*t,-ey] #start arc
        p7 = [-r2+0.5*t+r21,-ey+r2-r21] #second point arc
        p8 = [0.5*t,-ey+r2] #end arc
        p9 = [-p1[0],-p1[1]]
        p10 = [-p2[0],-p2[1]]
        p11 = [-p3[0],-p3[1]]
        p12 = [-p4[0],-p4[1]]
        p13 = [-p5[0],-p5[1]]
        p14 = [-p6[0],-p6[1]]
        p15 = [-p7[0],-p7[1]]
        p16 = [-p8[0],-p8[1]]

        l1 = Part.Arc(Vector(p1[0],p1[1],0),Vector(p2[0],p2[1],0),Vector(p3[0],p3[1],0))
        l1 = l1.toShape()
        l2 = Part.makeLine(Vector((p3[0]),p3[1],0),Vector(p4[0],p4[1],0))
        l3 = Part.makeLine(Vector((p4[0]),p4[1],0),Vector(p5[0],p5[1],0))
        l4 = Part.makeLine(Vector((p5[0]),p5[1],0),Vector(p6[0],p6[1],0))
        l5 = Part.Arc(Vector(p6[0],p6[1],0),Vector(p7[0],p7[1],0),Vector(p8[0],p8[1],0))
        l5 = l5.toShape()
        l6 = Part.makeLine(Vector((p8[0]),p8[1],0),Vector(p9[0],p9[1],0))
        l7 = Part.Arc(Vector(p9[0],p9[1],0),Vector(p10[0],p10[1],0),Vector(p11[0],p11[1],0))
        l7 = l7.toShape()
        l8 = Part.makeLine(Vector((p11[0]),p11[1],0),Vector(p12[0],p12[1],0))
        l9 = Part.makeLine(Vector((p12[0]),p12[1],0),Vector(p13[0],p13[1],0))
        l10 = Part.makeLine(Vector((p13[0]),p13[1],0),Vector(p14[0],p14[1],0))
        l11 = Part.Arc(Vector(p14[0],p14[1],0),Vector(p15[0],p15[1],0),Vector(p16[0],p16[1],0))
        l11 = l11.toShape()
        l12 = Part.makeLine(Vector((p16[0]),p16[1],0),Vector(p1[0],p1[1],0))

        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12])
        
        p = Part.Face(aWire)
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelCF_Z_WL(_Profile):

   '''Cold formed Z-profile with lips'''

   def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web and flange")).Thickness = profile[6]
        obj.addProperty("App::PropertyLength","InnerFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Inner fillet")).InnerFillet = profile[7]
        obj.addProperty("App::PropertyLength","LipLength","Draft",QT_TRANSLATE_NOOP("App::Property","Length of lip")).LipLength = profile[8]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = obj.Width.Value/2
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        
        _Profile.__init__(self,obj,profile)

   def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        t = obj.Thickness.Value
        h1 = obj.LipLength.Value
        r1 = obj.InnerFillet.Value
        r11 = r1/math.sqrt(2)
        r2 = r1+t
        r21 = r2/math.sqrt(2)
        ex = obj.CentroidHorizontal.Value #from left
        ey = obj.CentroidVertical.Value #from bottom

        pl = obj.Placement
        p1 = [-0.5*t,-ey+t+r1] #start arc
        p2 = [-0.5*t-r1+r11,-ey+t+r1-r11] #second point arc
        p3 = [-0.5*t-r1,-ey+t] #end arc
        p4 = [-ex+t+r1,-ey+t] #start arc
        p5 = [-ex+t+r1-r11,-ey+t+r1-r11] #second point arc
        p6 = [-ex+t,-ey+t+r1] #end arc
        p7 = [-ex+t,-ey+h1] 
        p8 = [-ex,-ey+h1]
        p9 = [-ex,-ey+r2] #start arc
        p10 = [-ex+r2-r21,-ey+r2-r21] #second point arc
        p11 = [-ex+r2,-ey] #end arc
        p12 = [-r2+0.5*t,-ey] #start arc
        p13 = [-r2+0.5*t+r21,-ey+r2-r21] #second point arc
        p14 = [0.5*t,-ey+r2] #end arc
        p15 = [-p1[0],-p1[1]]
        p16 = [-p2[0],-p2[1]]
        p17 = [-p3[0],-p3[1]]
        p18 = [-p4[0],-p4[1]]
        p19 = [-p5[0],-p5[1]]
        p20 = [-p6[0],-p6[1]]
        p21 = [-p7[0],-p7[1]]
        p22 = [-p8[0],-p8[1]]
        p23 = [-p9[0],-p9[1]]
        p24 = [-p10[0],-p10[1]]
        p25 = [-p11[0],-p11[1]]
        p26 = [-p12[0],-p12[1]]
        p27 = [-p13[0],-p13[1]]
        p28 = [-p14[0],-p14[1]]

        l1 = Part.Arc(Vector(p1[0],p1[1],0),Vector(p2[0],p2[1],0),Vector(p3[0],p3[1],0))
        l1 = l1.toShape()
        l2 = Part.makeLine(Vector((p3[0]),p3[1],0),Vector(p4[0],p4[1],0))
        l3 = Part.Arc(Vector(p4[0],p4[1],0),Vector(p5[0],p5[1],0),Vector(p6[0],p6[1],0))
        l3 = l3.toShape()
        l4 = Part.makeLine(Vector((p6[0]),p6[1],0),Vector(p7[0],p7[1],0))
        l5 = Part.makeLine(Vector((p7[0]),p7[1],0),Vector(p8[0],p8[1],0))
        l6 = Part.makeLine(Vector((p8[0]),p8[1],0),Vector(p9[0],p9[1],0))
        l7 = Part.Arc(Vector(p9[0],p9[1],0),Vector(p10[0],p10[1],0),Vector(p11[0],p11[1],0))
        l7 = l7.toShape()
        l8 = Part.makeLine(Vector((p11[0]),p11[1],0),Vector(p12[0],p12[1],0))
        l9 = Part.Arc(Vector(p12[0],p12[1],0),Vector(p13[0],p13[1],0),Vector(p14[0],p14[1],0))
        l9 = l9.toShape()
        l10 = Part.makeLine(Vector((p14[0]),p14[1],0),Vector(p15[0],p15[1],0))
        l11 = Part.Arc(Vector(p15[0],p15[1],0),Vector(p16[0],p16[1],0),Vector(p17[0],p17[1],0))
        l11 = l11.toShape()
        l12 = Part.makeLine(Vector((p17[0]),p17[1],0),Vector(p18[0],p18[1],0))
        l13 = Part.Arc(Vector(p18[0],p18[1],0),Vector(p19[0],p19[1],0),Vector(p20[0],p20[1],0))
        l13 = l13.toShape()
        l14 = Part.makeLine(Vector((p20[0]),p20[1],0),Vector(p21[0],p21[1],0))
        l15 = Part.makeLine(Vector((p21[0]),p21[1],0),Vector(p22[0],p22[1],0))
        l16 = Part.makeLine(Vector((p22[0]),p22[1],0),Vector(p23[0],p23[1],0))
        l17 = Part.Arc(Vector(p23[0],p23[1],0),Vector(p24[0],p24[1],0),Vector(p25[0],p25[1],0))
        l17 = l17.toShape()
        l18 = Part.makeLine(Vector((p25[0]),p25[1],0),Vector(p26[0],p26[1],0))
        l19 = Part.Arc(Vector(p26[0],p26[1],0),Vector(p27[0],p27[1],0),Vector(p28[0],p28[1],0))
        l19 = l19.toShape()
        l20 = Part.makeLine(Vector((p28[0]),p28[1],0),Vector(p1[0],p1[1],0))

        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17,l18,l19,l20])
        
        p = Part.Face(aWire)
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelHR_CHS(_Profile):

    '''A parametric circular tubeprofile. Profile data: [Outside diameter, Inside diameter]'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","OutDiameter","Draft",QT_TRANSLATE_NOOP("App::Property","Outside Diameter")).OutDiameter = profile[4]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Wall thickness")).Thickness = profile[5]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = obj.OutDiameter.Value/2
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.OutDiameter.Value/2
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = obj.OutDiameter.Value
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = obj.OutDiameter.Value

        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        pl = obj.Placement
        c1 = Part.Circle()
        c1.Radius=obj.OutDiameter.Value/2
        c2 = Part.Circle()
        c2.Radius=obj.OutDiameter.Value/2-obj.Thickness.Value
        cs1 = c1.toShape()
        cs2 = c2.toShape()
        p = Part.makeRuledSurface(cs2,cs1)
        p.reverse()
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelHR_RS(_Profile):

    '''Steel Round Section'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Diameter","Draft",QT_TRANSLATE_NOOP("App::Property","Diameter")).Diameter = profile[4]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = obj.Diameter.Value/2
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Diameter.Value/2
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = obj.Diameter.Value
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = obj.Diameter.Value

        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        pl = obj.Placement
        c1 = Part.Circle()
        c1.Radius=obj.Diameter.Value/2
        cs1 = c1.toShape()
        p = Part.face(cs1)
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelHR_L(_Profile):

    '''A parametric L-angle. Profile data: [NTB]'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web and flange")).Thickness = profile[6]
        obj.addProperty("App::PropertyLength","OuterFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Outer fillet")).OuterFillet = profile[7]
        obj.addProperty("App::PropertyLength","WebFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Inner fillet between web and flange")).WebFillet = profile[8]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = profile[9]
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = profile[10]
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        tf = obj.Thickness.Value
        tw = tf
        r1 = obj.WebFillet.Value
        r11 = r1/math.sqrt(2)
        r2 = obj.OuterFillet.Value
        r21 = r2/math.sqrt(2)
        ex = obj.CentroidHorizontal.Value #from left
        ey = obj.CentroidVertical.Value #from bottom

        pl = obj.Placement
        p1 = [-ex,-ey] #left bottom
        p2 = [b-ex,-ey] #right bottom
        p3 = [b-ex,-ey+tf-r2] #start arc
        p4 = [b-ex-r2+r21,-ey+tf-r2+r21] #second point arc
        p5 = [b-ex-r2,-ey+tf] #end arc
        p6 = [-ex+tf+r1,-ey+tf] #start arc
        p7 = [-ex+tf+r1-r11,-ey+tf+r1-r11] #second point arc
        p8 = [-ex+tf,-ey+tf+r1] #end arc
        p9 = [-ex+tf,h-ey-r2] #start arc
        p10 = [-ex+tf-r2+r21,h-ey-r2+r21] #second point arc
        p11 = [-ex+tf-r2,h-ey] #end arc
        p12 = [-ex,h-ey] #left top

        l1 = Part.makeLine(Vector((p1[0]),p1[1],0),Vector(p2[0],p2[1],0))
        l2 = Part.makeLine(Vector((p2[0]),p2[1],0),Vector(p3[0],p3[1],0))
        l3 = Part.Arc(Vector(p3[0],p3[1],0),Vector(p4[0],p4[1],0),Vector(p5[0],p5[1],0))
        l3 = l3.toShape()
        l4 = Part.makeLine(Vector((p5[0]),p5[1],0),Vector(p6[0],p6[1],0))
        l5 = Part.Arc(Vector(p6[0],p6[1],0),Vector(p7[0],p7[1],0),Vector(p8[0],p8[1],0))
        l5 = l5.toShape()
        l6 = Part.makeLine(Vector((p8[0]),p8[1],0),Vector(p9[0],p9[1],0))
        l7 = Part.Arc(Vector(p9[0],p9[1],0),Vector(p10[0],p10[1],0),Vector(p11[0],p11[1],0))
        l7 = l7.toShape()
        l8 = Part.makeLine(Vector((p11[0]),p11[1],0),Vector(p12[0],p12[1],0))
        l9 = Part.makeLine(Vector((p12[0]),p12[1],0),Vector(p1[0],p1[1],0))
        
        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9])
        
        p = Part.Face(aWire)
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelHR_I_PF(_Profile):

    '''A parametric H or I beam profile. Profile data: [width, height, web thickness, flange thickness, radius] (see http://en.wikipedia.org/wiki/I-beam for reference)'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","WebThickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web")).WebThickness = profile[6]
        obj.addProperty("App::PropertyLength","FlangeThickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the flanges")).FlangeThickness = profile[7]
        obj.addProperty("App::PropertyLength","Radius","Draft",QT_TRANSLATE_NOOP("App::Property","Web Filled")).Radius = profile[8]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = obj.Width.Value/2
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        tf = obj.FlangeThickness.Value
        tw = obj.WebThickness.Value
        r = obj.Radius.Value
        r1 = r/math.sqrt(2)

        pl = obj.Placement
        p1 = Vector((-b/2),(-h/2))#left bottom
        p2 = Vector((b/2),(-h/2))#right bottom
        p3 = Vector((b/2),(-h/2+tf))
        p4 = Vector(tw/2+r,-h/2+tf)#start arc
        p4_5 = [tw/2+r-r1,(-h/2+tf+r-r1)]#second point arc
        p5 = Vector((tw/2),(-h/2+tf+r))#end arc
        p6 = Vector((tw/2),(h/2-tf-r))#start arc
        p6_7 = [tw/2+r-r1,(h/2-tf-r+r1)]#second point arc
        p7 = Vector((tw/2+r),(h/2-tf))#end arc
        p8 = Vector((b/2),(h/2-tf))
        p9 = Vector((b/2),(h/2))#right top
        p10 = Vector((-b/2),(h/2))#left top
        p11 = Vector((-b/2),(h/2-tf))
        p12 = Vector(-(tw/2)-r,(h/2-tf))#start arc
        p12_13 = [-tw/2-r+r1,(h/2-tf-r+r1)]#second point arc
        p13 = Vector(-(tw/2),(h/2-tf-r))#end arc
        p14 = Vector(-(tw/2),-(h/2-tf-r))#start arc
        p14_15 = [-tw/2-r+r1,(-h/2+tf+r-r1)]#second point arc
        p15 = Vector(-(tw/2)-r,-(h/2-tf))#end arc
        p16 = Vector(-(b/2),-(h/2-tf))

        l1 = Part.makeLine(Vector((p1[0]),p1[1],0),Vector(p2[0],p2[1],0))
        l2 = Part.makeLine(Vector((p2[0]),p2[1],0),Vector(p3[0],p3[1],0))
        l3 = Part.makeLine(Vector((p3[0]),p3[1],0),Vector(p4[0],p4[1],0))
        l4 = Part.Arc(Vector(p4[0],p4[1],0),Vector(p4_5[0],p4_5[1],0),Vector(p5[0],p5[1],0))
        l4 = l4.toShape()
        l5 = Part.makeLine(Vector((p5[0]),p5[1],0),Vector(p6[0],p6[1],0))
        l6 = Part.Arc(Vector(p6[0],p6[1],0),Vector(p6_7[0],p6_7[1],0),Vector(p7[0],p7[1],0))
        l6 = l6.toShape()
        l7 = Part.makeLine(Vector((p7[0]),p7[1],0),Vector(p8[0],p8[1],0))
        l8 = Part.makeLine(Vector((p8[0]),p8[1],0),Vector(p9[0],p9[1],0))
        l9 = Part.makeLine(Vector((p9[0]),p9[1],0),Vector(p10[0],p10[1],0))
        l10 = Part.makeLine(Vector((p10[0]),p10[1],0),Vector(p11[0],p11[1],0))
        l11 = Part.makeLine(Vector((p11[0]),p11[1],0),Vector(p12[0],p12[1],0))
        l12 = Part.Arc(Vector(p12[0],p12[1],0),Vector(p12_13[0],p12_13[1],0),Vector(p13[0],p13[1],0))
        l12 = l12.toShape()
        l13 = Part.makeLine(Vector((p13[0]),p13[1],0),Vector(p14[0],p14[1],0))
        l14 = Part.Arc(Vector(p14[0],p14[1],0),Vector(p14_15[0],p14_15[1],0),Vector(p15[0],p15[1],0))
        l14 = l14.toShape()
        l15 = Part.makeLine(Vector((p15[0]),p15[1],0),Vector(p16[0],p16[1],0))
        l16 = Part.makeLine(Vector((p16[0]),p16[1],0),Vector(p1[0],p1[1],0))
        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16])
        
        p = Part.Face(aWire)
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelHR_I_SF(_Profile):

    '''A parametric I/H beam profile with sloped flanges.'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","WebThickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the webs")).WebThickness = profile[6]
        obj.addProperty("App::PropertyLength","FlangeThickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the flange")).FlangeThickness = profile[7]
        obj.addProperty("App::PropertyLength","WebFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Web fillet")).WebFillet = profile[8]
        obj.addProperty("App::PropertyLength","FlangeFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Flange fillet")).FlangeFillet = profile[9]
        obj.addProperty("App::PropertyLength","FlangeThicknessLocation","Draft",QT_TRANSLATE_NOOP("App::Property","Location of the flange thickness from the right")).FlangeThicknessLocation = profile[10]
        obj.addProperty("App::PropertyAngle","SlopedFlangeAngle","Draft",QT_TRANSLATE_NOOP("App::Property","Angle of the sloped flange")).SlopedFlangeAngle = profile[11]      
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = obj.Width.Value/2
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        tf = obj.FlangeThickness.Value
        tw = obj.WebThickness.Value
        r1 = obj.WebFillet.Value
        r11 = r1/math.sqrt(2)
        r2 = obj.FlangeFillet.Value
        r21 = r2/math.sqrt(2)
        tl = obj.FlangeThicknessLocation.Value
        sa = math.radians(obj.SlopedFlangeAngle.Value)
        ex = b/2
        ey = h/2

        #describe points
        pl = obj.Placement
        p1 = [ex,-ey] #right bottom
        p2 = [ex,-ey+tf-math.tan(sa)*(tl-r2+math.sin(sa)*r2)-r2] #start arc
        p3 = [ex-r2+r21,-ey+tf-math.tan(sa)*(tl-r2+math.sin(sa)*r2)-r2+r21] #second point arc
        p4 = [ex-r2+math.sin(sa)*r2,-ey+tf-math.tan(sa)*(tl-r2+math.sin(sa)*r2)] #end arc
        p5 = [tw/2+r1-math.sin(sa)*r1,-ey+tf+math.tan(sa)*(ex-tl-0.5*tw-r1+math.sin(sa)*r1)] #start arc
        p6 = [tw/2+r1-r11,-h/2+tf+math.tan(sa)*(0.5*b-tl-tw-r1)+r1-r11] #second point arc
        p7 = [tw/2,-h/2+tf+math.tan(sa)*(ex-tl-0.5*tw-r1+math.sin(sa)*r1)+r1] #end arc
        
        p8 = [p7[0],-p7[1]]
        p9 = [p6[0],-p6[1]]
        p10 = [p5[0],-p5[1]]
        p11 = [p4[0],-p4[1]]
        p12 = [p3[0],-p3[1]]
        p13 = [p2[0],-p2[1]]
        p14 = [p1[0],-p1[1]]

        p15 = [-p14[0],p14[1]]
        p16 = [-p13[0],p13[1]]
        p17 = [-p12[0],p12[1]]
        p18 = [-p11[0],p11[1]]
        p19 = [-p10[0],p10[1]]
        p20 = [-p9[0],p9[1]]
        p21 = [-p8[0],p8[1]]

        p22 = [-p7[0],p7[1]]
        p23 = [-p6[0],p6[1]]
        p24 = [-p5[0],p5[1]]
        p25 = [-p4[0],p4[1]]
        p26 = [-p3[0],p3[1]]
        p27 = [-p2[0],p2[1]]
        p28 = [-p1[0],p1[1]]
      
        #Lines and arcs
        l1 = Part.makeLine(Vector((p1[0]),p1[1],0),Vector(p2[0],p2[1],0))
        l2 = Part.Arc(Vector(p2[0],p2[1],0),Vector(p3[0],p3[1],0),Vector(p4[0],p4[1],0))
        l2 = l2.toShape()
        l3 = Part.makeLine(Vector((p4[0]),p4[1],0),Vector(p5[0],p5[1],0))
        l4 = Part.Arc(Vector(p5[0],p5[1],0),Vector(p6[0],p6[1],0),Vector(p7[0],p7[1],0))
        l4 = l4.toShape()
        l5 = Part.makeLine(Vector((p7[0]),p7[1],0),Vector(p8[0],p8[1],0))
        l6 = Part.Arc(Vector(p8[0],p8[1],0),Vector(p9[0],p9[1],0),Vector(p10[0],p10[1],0))
        l6 = l6.toShape()
        l7 = Part.makeLine(Vector((p10[0]),p10[1],0),Vector(p11[0],p11[1],0))
        l8 = Part.Arc(Vector(p11[0],p11[1],0),Vector(p12[0],p12[1],0),Vector(p13[0],p13[1],0))
        l8 = l8.toShape()
        l9 = Part.makeLine(Vector((p13[0]),p13[1],0),Vector(p14[0],p14[1],0))
        l10 = Part.makeLine(Vector((p14[0]),p14[1],0),Vector(p15[0],p15[1],0))      
        l11 = Part.makeLine(Vector((p15[0]),p15[1],0),Vector(p16[0],p16[1],0))
        l12 = Part.Arc(Vector(p16[0],p16[1],0),Vector(p17[0],p17[1],0),Vector(p18[0],p18[1],0))
        l12 = l12.toShape()
        l13 = Part.makeLine(Vector((p18[0]),p18[1],0),Vector(p19[0],p19[1],0))
        l14 = Part.Arc(Vector(p19[0],p19[1],0),Vector(p20[0],p20[1],0),Vector(p21[0],p21[1],0))
        l14 = l14.toShape()
        l15 = Part.makeLine(Vector((p21[0]),p21[1],0),Vector(p22[0],p22[1],0))
        l16 = Part.Arc(Vector(p22[0],p22[1],0),Vector(p23[0],p23[1],0),Vector(p24[0],p24[1],0))
        l16 = l16.toShape()
        l17 = Part.makeLine(Vector((p24[0]),p24[1],0),Vector(p25[0],p25[1],0))
        l18 = Part.Arc(Vector(p25[0],p25[1],0),Vector(p26[0],p26[1],0),Vector(p27[0],p27[1],0))
        l18 = l18.toShape()
        l19 = Part.makeLine(Vector((p27[0]),p27[1],0),Vector(p28[0],p28[1],0))
        l20 = Part.makeLine(Vector((p28[0]),p28[1],0),Vector(p1[0],p1[1],0))

        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17,l18,l19,l20])

        p = Part.Face(aWire)
        #p.reverse()
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelHR_RCT(_Profile):

    '''A parametric rectangular beam profile based on [Width, Height]'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = obj.Width.Value/2
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        pl = obj.Placement
        p1 = Vector(-obj.Width.Value/2,-obj.Height.Value/2,0)
        p2 = Vector(obj.Width.Value/2,-obj.Height.Value/2,0)
        p3 = Vector(obj.Width.Value/2,obj.Height.Value/2,0)
        p4 = Vector(-obj.Width.Value/2,obj.Height.Value/2,0)
        p = Part.makePolygon([p1,p2,p3,p4,p1])
        p = Part.Face(p)
        #p.reverse()
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelHR_RHS(_Profile):

    '''A parametric Rectangular hollow beam profile. Profile data: [width, height, thickness, outer fillet, inner fillet]'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the sides")).Thickness = profile[6]
        obj.addProperty("App::PropertyLength","OuterFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Outer fillet")).OuterFillet = profile[7]
        obj.addProperty("App::PropertyLength","InnerFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Inner fillet")).InnerFillet = profile[8]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = obj.Width.Value/2
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value #width
        h = obj.Height.Value #height
        t = obj.Thickness.Value #wall nominal thickness
        r1 = obj.OuterFillet.Value #outer fillet
        r11 = r1/math.sqrt(2)
        r2 = obj.InnerFillet.Value #inner fillet
        r21 = r2/math.sqrt(2)

        #outer curve
        pl = obj.Placement
        p1 = [b/2-r1,-h/2] #right bottom start arc
        p2 = [b/2-r1+r11,-h/2+r1-r11] #right bottom second point arc
        p3 = [b/2,-h/2+r1] #right bottom end arc
        p4 = [p3[0],-p3[1]] #right top start arc
        p5 = [p2[0],-p2[1]] #right top second point arc
        p6 = [p1[0],-p1[1]] #right top end arc
        p7 = [-p6[0],p6[1]] #left top start arc
        p8 = [-p5[0],p5[1]] #left top second point arc
        p9 = [-p4[0],p4[1]] #left top end arc
        p10 = [p9[0],-p9[1]] #left bottom start arc
        p11 = [p8[0],-p8[1]] #left bottom second point arc
        p12 = [p7[0],-p7[1]] #left bottom end arc

        l1 = Part.Arc(Vector(p1[0],p1[1],0),Vector(p2[0],p2[1],0),Vector(p3[0],p3[1],0))
        l1 = l1.toShape()
        l2 = Part.makeLine(Vector((p3[0]),p3[1],0),Vector(p4[0],p4[1],0))
        l3 = Part.Arc(Vector(p4[0],p4[1],0),Vector(p5[0],p5[1],0),Vector(p6[0],p6[1],0))
        l3 = l3.toShape()
        l4 = Part.makeLine(Vector((p6[0]),p6[1],0),Vector(p7[0],p7[1],0))
        l5 = Part.Arc(Vector(p7[0],p7[1],0),Vector(p8[0],p8[1],0),Vector(p9[0],p9[1],0))
        l5 = l5.toShape()
        l6 = Part.makeLine(Vector((p9[0]),p9[1],0),Vector(p10[0],p10[1],0))
        l7 = Part.Arc(Vector(p10[0],p10[1],0),Vector(p11[0],p11[1],0),Vector(p12[0],p12[1],0))
        l7 = l7.toShape()
        l8 = Part.makeLine(Vector((p12[0]),p12[1],0),Vector(p1[0],p1[1],0))

        aWireOuter = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8])

        #inner curve
        q1 = [b/2-t-r2,-h/2+t] #right bottom start arc
        q2 = [b/2-t-r2+r21,-h/2+t+r2-r21] #right bottom second point arc
        q3 = [b/2-t,-h/2+t+r2] #right bottom end arc
        q4 = [q3[0],-q3[1]] #right top start arc
        q5 = [q2[0],-q2[1]] #right top second point arc
        q6 = [q1[0],-q1[1]] #right top end arc
        q7 = [-q6[0],q6[1]] #left top start arc
        q8 = [-q5[0],q5[1]] #left top second point arc
        q9 = [-q4[0],q4[1]] #left top end arc
        q10 = [q9[0],-q9[1]] #left bottom start arc
        q11 = [q8[0],-q8[1]] #left bottom second point arc
        q12 = [q7[0],-q7[1]] #left bottom end arc

        l21 = Part.Arc(Vector(q1[0],q1[1],0),Vector(q2[0],q2[1],0),Vector(q3[0],q3[1],0))
        l21 = l21.toShape()
        l22 = Part.makeLine(Vector((q3[0]),q3[1],0),Vector(q4[0],q4[1],0))
        l23 = Part.Arc(Vector(q4[0],q4[1],0),Vector(q5[0],q5[1],0),Vector(q6[0],q6[1],0))
        l23 = l23.toShape()
        l24 = Part.makeLine(Vector((q6[0]),q6[1],0),Vector(q7[0],q7[1],0))
        l25 = Part.Arc(Vector(q7[0],q7[1],0),Vector(q8[0],q8[1],0),Vector(q9[0],q9[1],0))
        l25 = l25.toShape()
        l26 = Part.makeLine(Vector((q9[0]),q9[1],0),Vector(q10[0],q10[1],0))
        l27 = Part.Arc(Vector(q10[0],q10[1],0),Vector(q11[0],q11[1],0),Vector(q12[0],q12[1],0))
        l27 = l27.toShape()
        l28 = Part.makeLine(Vector((q12[0]),q12[1],0),Vector(q1[0],q1[1],0))

        aWireInner = Part.Wire([l21,l22,l23,l24,l25,l26,l27,l28])

        p = Part.Face(aWireOuter)
        q = Part.Face(aWireInner)
        r = p.cut(q)
        obj.Shape = r
        obj.Placement = pl

class _Profile_SteelHR_C_PF(_Profile):

    '''A parametric U beam profile with parallel flanges. Profile data: [width, height, web thickness, flange thickness, radius, centroid horizontal] (see  http://en.wikipedia.org/wiki/I-beam for reference)'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","WebThickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web")).WebThickness = profile[6]
        obj.addProperty("App::PropertyLength","FlangeThickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the flange")).FlangeThickness = profile[7]
        obj.addProperty("App::PropertyLength","WebFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Web fillet")).WebFillet = profile[8]
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = profile[9]
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        tf = obj.FlangeThickness.Value
        tw = obj.WebThickness.Value
        r = obj.WebFillet.Value
        r1 = r/math.sqrt(2)
        e = obj.CentroidHorizontal.Value
        
        #Points
        pl = obj.Placement
        p1 = [-e,-h/2,0] #left bottom
        p2 = [b-e,-h/2,0] #right bottom
        p3 = [b-e,-h/2+tf,0] 
        p4 = [-e+tw+r,-h/2+tf,0] #start arc
        p5 = [-e+tw+r-r1,-h/2+tf+r-r1,0] #second point arc
        p6 = [-e+tw,-h/2+tf+r,0] #end arc
        p7 = [-e+tw,h/2-tf-r,0] #start arc
        p8 = [-e+tw+r-r1,h/2-tf-r+r1,0] #second point arc
        p9 = [-e+tw+r,h/2-tf,0] #end arc
        p10 = [b-e,h/2-tf,0]
        p11 = [b-e,h/2,0] #right top
        p12 = [-e,h/2,0] #left top
        
        #Lines and arcs
        l1 = Part.makeLine(Vector((p1[0]),p1[1],0),Vector(p2[0],p2[1],0))
        l2 = Part.makeLine(Vector((p2[0]),p2[1],0),Vector(p3[0],p3[1],0))
        l3 = Part.makeLine(Vector((p3[0]),p3[1],0),Vector(p4[0],p4[1],0))
        l4 = Part.Arc(Vector(p4[0],p4[1],0),Vector(p5[0],p5[1],0),Vector(p6[0],p6[1],0))
        l4 = l4.toShape()
        l5 = Part.makeLine(Vector((p6[0]),p6[1],0),Vector(p7[0],p7[1],0))
        l6 = Part.Arc(Vector(p7[0],p7[1],0),Vector(p8[0],p8[1],0),Vector(p9[0],p9[1],0))
        l6 = l6.toShape()
        l7 = Part.makeLine(Vector((p9[0]),p9[1],0),Vector(p10[0],p10[1],0))
        l8 = Part.makeLine(Vector((p10[0]),p10[1],0),Vector(p11[0],p11[1],0))
        l9 = Part.makeLine(Vector((p11[0]),p11[1],0),Vector(p12[0],p12[1],0))
        l10 = Part.makeLine(Vector((p12[0]),p12[1],0),Vector(p1[0],p1[1],0)) 

        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10])

        p = Part.Face(aWire)
        #p.reverse()
        obj.Shape = p
        obj.Placement = pl

class _Profile_SteelHR_C_SF(_Profile):

    '''A parametric U beam profile with sloped flanges. Profile data: [width, height, web thickness, flange thickness, web fillet, flange fillet, centroid horizontal] (see  http://en.wikipedia.org/wiki/I-beam for reference)'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","WebThickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the webs")).WebThickness = profile[6]
        obj.addProperty("App::PropertyLength","FlangeThickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the flange")).FlangeThickness = profile[7]
        obj.addProperty("App::PropertyLength","WebFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Web fillet")).WebFillet = profile[8]
        obj.addProperty("App::PropertyLength","FlangeFillet","Draft",QT_TRANSLATE_NOOP("App::Property","Flange fillet")).FlangeFillet = profile[9]
        obj.addProperty("App::PropertyLength","FlangeThicknessLocation","Draft",QT_TRANSLATE_NOOP("App::Property","Location of the flange thickness from the right")).FlangeThicknessLocation = profile[10]
        obj.addProperty("App::PropertyAngle","SlopedFlangeAngle","Draft",QT_TRANSLATE_NOOP("App::Property","Angle of the sloped flange")).SlopedFlangeAngle = profile[11]      
        obj.addProperty("App::PropertyLength","CentroidHorizontal","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid horizontal")).CentroidHorizontal = profile[12]
        obj.addProperty("App::PropertyLength","CentroidVertical","Draft",QT_TRANSLATE_NOOP("App::Property","Centroid vertical")).CentroidVertical = obj.Height.Value/2
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        import Draft
        import math

        b = obj.Width.Value
        h = obj.Height.Value
        tf = obj.FlangeThickness.Value
        tw = obj.WebThickness.Value
        r1 = obj.WebFillet.Value
        r11 = r1/math.sqrt(2)
        r2 = obj.FlangeFillet.Value
        r21 = r2/math.sqrt(2)
        tl = obj.FlangeThicknessLocation.Value
        sa = math.radians(obj.SlopedFlangeAngle.Value)
        e = obj.CentroidHorizontal.Value

        #describe points
        pl = obj.Placement
        p1 = [-e,-h/2] #left bottom
        p2 = [b-e,-h/2] #right bottom
        p3 = [b-e,-h/2+tf-math.tan(sa)*tl-r2] #start arc
        p4 = [b-e-r2+r21,-h/2+tf-math.tan(sa)*tl-r2+r21] #second point arc
        p5 = [b-e-r2+math.sin(sa)*r2,-h/2+tf-math.tan(sa)*(tl-r2)] #end arc
        p6 = [-e+tw+r1-math.sin(sa)*r1,-h/2+tf+math.tan(sa)*(b-tl-tw-r1)] #start arc
        p7 = [-e+tw+r1-r11,-h/2+tf+math.tan(sa)*(b-tl-tw-r1)+r1-r11] #second point arc
        p8 = [-e+tw,-h/2+tf+math.tan(sa)*(b-tl-tw)+r1] #end arc
        p9 = [p8[0],-p8[1]] #start arc
        p10 = [p7[0],-p7[1]] #second point arc
        p11 = [p6[0],-p6[1]] #end arc
        p12 = [p5[0],-p5[1]] #start arc
        p13 = [p4[0],-p4[1]] #second point arc
        p14 = [p3[0],-p3[1]] #end arc
        p15 = [p2[0],-p2[1]] #right top
        p16 = [p1[0],-p1[1]] #left top

       
        #Lines and arcs
        l1 = Part.makeLine(Vector((p1[0]),p1[1],0),Vector(p2[0],p2[1],0))
        l2 = Part.makeLine(Vector((p2[0]),p2[1],0),Vector(p3[0],p3[1],0))
        l3 = Part.Arc(Vector(p3[0],p3[1],0),Vector(p4[0],p4[1],0),Vector(p5[0],p5[1],0))
        l3 = l3.toShape()
        l4 = Part.makeLine(Vector((p5[0]),p5[1],0),Vector(p6[0],p6[1],0))
        l5 = Part.Arc(Vector(p6[0],p6[1],0),Vector(p7[0],p7[1],0),Vector(p8[0],p8[1],0))
        l5 = l5.toShape()
        l6 = Part.makeLine(Vector((p8[0]),p8[1],0),Vector(p9[0],p9[1],0))
        l7 = Part.Arc(Vector(p9[0],p9[1],0),Vector(p10[0],p10[1],0),Vector(p11[0],p11[1],0))
        l7 = l7.toShape()
        l8 = Part.makeLine(Vector((p11[0]),p11[1],0),Vector(p12[0],p12[1],0))
        l9 = Part.Arc(Vector(p12[0],p12[1],0),Vector(p13[0],p13[1],0),Vector(p14[0],p14[1],0))
        l9 = l9.toShape()
        l10 = Part.makeLine(Vector((p14[0]),p14[1],0),Vector(p15[0],p15[1],0))
        l11 = Part.makeLine(Vector((p15[0]),p15[1],0),Vector(p16[0],p16[1],0))
        l12 = Part.makeLine(Vector((p16[0]),p16[1],0),Vector(p1[0],p1[1],0))

        aWire = Part.Wire([l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12])

        p = Part.Face(aWire)
        #p.reverse()
        obj.Shape = p
        obj.Placement = pl

class ViewProviderProfile(Draft._ViewProviderDraft):

    '''General view provider for Profile classes'''

    def __init__(self,vobj):

        Draft._ViewProviderDraft.__init__(self,vobj)

    def getIcon(self):

        import Arch_rc
        return ":/icons/Arch_Profile.svg"

    def setEdit(self,vobj,mode):

        taskd = ProfileTaskPanel(vobj.Object)
        FreeCADGui.Control.showDialog(taskd)
        return True

    def unsetEdit(self,vobj,mode):

        FreeCADGui.Control.closeDialog()
        FreeCAD.ActiveDocument.recompute()
        return

class ProfileTaskPanel:

    '''The editmode TaskPanel for Profile objects'''

    def __init__(self,obj):

        self.obj = obj
        self.profile = None
        if isinstance(self.obj.Proxy,_Profile_Generic_RCT):
            self.type = "Generic_RCT"
        elif isinstance(self.obj.Proxy,_Profile_SteelCF_C):
            self.type = "SteelCF_C"
        elif isinstance(self.obj.Proxy,_Profile_SteelCF_C_WL):
            self.type = "SteelCF_C_WL" 
        elif isinstance(self.obj.Proxy,_Profile_SteelCF_L):
            self.type = "SteelCF_L" 
        elif isinstance(self.obj.Proxy,_Profile_SteelCF_Sigma_WL):
            self.type = "SteelCF_Sigma_WL"
        elif isinstance(self.obj.Proxy,_Profile_SteelCF_Z):
            self.type = "SteelCF_Z"
        elif isinstance(self.obj.Proxy,_Profile_SteelCF_Z_WL):
            self.type = "SteelCF_Z_WL" 
        elif isinstance(self.obj.Proxy,_Profile_SteelHR_CHS):
            self.type = "SteelHR_CHS"
        elif isinstance(self.obj.Proxy,_Profile_SteelHR_I_PF):
            self.type = "SteelHR_I_PF"
        elif isinstance(self.obj.Proxy,_Profile_SteelHR_I_SF):
            self.type = "SteelHR_I_SF"
        elif isinstance(self.obj.Proxy,_Profile_SteelHR_L):
            self.type = "SteelHR_L"
        elif isinstance(self.obj.Proxy,_Profile_SteelHR_RS):
            self.type = "SteelHR_RS"
        elif isinstance(self.obj.Proxy,_Profile_SteelHR_RHS):
            self.type = "SteelHR_RHS"
        elif isinstance(self.obj.Proxy,_Profile_SteelHR_RCT):
            self.type = "SteelHR_RCT"
        elif isinstance(self.obj.Proxy,_Profile_SteelHR_C_PF):
            self.type = "SteelHR_C_PF"
        elif isinstance(self.obj.Proxy,_Profile_SteelHR_C_SFF):
            self.type = "SteelHR_C_SF"
        else:
            self.type = "Undefined"
        self.form = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(self.form)
        self.comboCategory = QtGui.QComboBox(self.form)
        layout.addWidget(self.comboCategory)
        self.comboProfile = QtGui.QComboBox(self.form)
        layout.addWidget(self.comboProfile)
        QtCore.QObject.connect(self.comboCategory, QtCore.SIGNAL("currentIndexChanged(QString)"), self.changeCategory)
        QtCore.QObject.connect(self.comboProfile, QtCore.SIGNAL("currentIndexChanged(int)"), self.changeProfile)
        # Read preset profiles and add relevant ones
        self.categories=[]
        self.presets=readPresets()
        for pre in self.presets:
            if pre[3] == self.type:
                if pre[1] not in self.categories:
                    self.categories.append(pre[1])
        self.comboCategory.addItem(" ")
        if self.categories:
            self.comboCategory.addItems(self.categories)
        # Find current profile by label
        for pre in self.presets:
            if self.obj.Label in pre[2]:
                self.profile = pre
                break
        if not self.profile:
            # try to find by size
            if hasattr(self.obj,"Width") and hasattr(self.obj,"Height"):
                for pre in self.presets:
                    if abs(self.obj.Width - self.Profile[4]) < 0.1 and \
                       abs(self.obj.Height - self.Profile[5]) < 0.1:
                        self.profile = pre
                        break
        if self.profile:
            origprofile = list(self.profile) # the operation below will change self.profile
            self.comboCategory.setCurrentIndex(1+self.categories.index(origprofile[1]))
            self.changeCategory(origprofile[1])
            self.comboProfile.setCurrentIndex(self.currentpresets.index(origprofile))
        self.retranslateUi(self.form)

    def changeCategory(self,text):

        self.comboProfile.clear()
        self.currentpresets = []
        for pre in self.presets:
            if pre[1] == text:
                self.currentpresets.append(pre)
                f = FreeCAD.Units.Quantity(pre[4],FreeCAD.Units.Length).getUserPreferred()
                d = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt("Decimals",2)
                s1 = str(round(pre[4]/f[1],d))
                s2 = str(round(pre[5]/f[1],d))
                s3 = str(f[2])
                self.comboProfile.addItem(pre[2]+" ("+s1+"x"+s2+s3+")")

    def changeProfile(self,idx):

        self.profile = self.currentpresets[idx]

    def accept(self):

        if self.profile:
            self.obj.Label = self.profile[2]
            if self.type in ["Generic_RCT","SteelCF_C","SteelCF_C_WL","SteelCF_L","SteelCF_Sigma_WL","SteelCF_Z","SteelCF_Z_WL","SteelHR_C_PF","SteelHR_C_SF","SteelHR_I_PF","SteelHR_I_SF","SteelHR_L","SteelHR_RHS","SteelHR_RCT","SteelHR_CHS","SteelHR_CHS"]:
                self.obj.Width = self.profile[4]
                self.obj.Height = self.profile[5]
                if self.type in ["H","U","U2"]:
                    self.obj.WebThickness = self.profile[6]
                    self.obj.FlangeThickness = self.profile[7]
                elif self.type == "RH":
                    self.obj.Thickness = self.profile[6]
            elif self.type == "SteelHR_CHS":
                self.obj.OutDiameter = self.profile[4]
                self.obj.Thickness = self.profile[5]
            FreeCAD.ActiveDocument.recompute()
            FreeCADGui.ActiveDocument.resetEdit()
        return True

    def retranslateUi(self, TaskPanel):

        self.form.setWindowTitle(self.type+" "+QtGui.QApplication.translate("Arch", "Profile", None))
