import math

#p10 --------------------- p9
#	|					|
#p11 ---------   --------- p8
#		p12	 | | p7
#		p13	 | | p6
#			 | |
#			 | |
#		p14  | | p5
#		p15	 | | p4
#p16 ---------   --------- p3
#	|					|
#p1	--------------------- p2


p1 = [(-b/2),(-h/2)] #left bottom
p2 = [(b/2),(-h/2)] #right bottom
p3 = [(b/2),(-h/2+tf)]
p4 = [(tw/2+r),(-h/2+tf)]#start arc
p5 = [(tw/2),(-h/2+tf+r)]#end arc
p6 = [(tw/2),(h/2-tf-r)]#start arc
p7 = [(tw/2+r),(h/2-tf)]#end arc
p8 = [(b/2),(h/2-tf)]
p9 = [(b/2),(h/2)] #right top
p10 = [(-b/2),(h/2)] #left top
p11 = [(-b/2),(h/2-tf)]
p12 = [-(tw/2)-r,(h/2-tf)]#start arc
p13 = [-(tw/2),(h/2-tf-r)]#end arc
p14 = [-(tw/2),-(h/2-tf-r)]#start arc
p15 = [-(tw/2)-r,-(h/2-tf)]#end arc
p16 = [-(b/2),-(h/2-tf)]

sketch_name = "HEA200"

#FREECAD COMMANDS

x = 2000
y = 3000

Gui.activateWorkbench("SketcherWorkbench")
App.activeDocument().addObject('Sketcher::SketchObject','HEA200')
App.activeDocument().HEA200.Placement = App.Placement(App.Vector(x,y,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
App.activeDocument().HEA200.MapMode = "Deactivated"
Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
Gui.activeDocument().setEdit('HEA200')
ActiveSketch = App.ActiveDocument.getObject('HEA200')
tv = Show.TempoVis(App.ActiveDocument)
if ActiveSketch.ViewObject.HideDependent:
    objs = tv.get_all_dependent(ActiveSketch)
    objs = filter(lambda x: not x.TypeId.startswith("TechDraw::"), objs)
    objs = filter(lambda x: not x.TypeId.startswith("Drawing::"), objs)
    tv.hide(objs)
if ActiveSketch.ViewObject.ShowSupport:
    tv.show([ref[0] for ref in ActiveSketch.Support if not ref[0].isDerivedFrom("PartDesign::Plane")])
if ActiveSketch.ViewObject.ShowLinks:
    tv.show([ref[0] for ref in ActiveSketch.ExternalGeometry])
tv.hide(ActiveSketch)
ActiveSketch.ViewObject.TempoVis = tv
del(tv)

ActiveSketch = App.ActiveDocument.getObject('HEA200')
if ActiveSketch.ViewObject.RestoreCamera:
    ActiveSketch.ViewObject.TempoVis.saveCamera()

App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p1[0]),p1[1],0),App.Vector(p2[0],p2[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p2[0]),p2[1],0),App.Vector(p3[0],p3[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p3[0]),p3[1],0),App.Vector(p4[0],p4[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p4[0],p5[1],0),App.Vector(0,0,1),r),(-math.pi),(-math.pi*0.5)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p5[0]),p5[1],0),App.Vector(p6[0],p6[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p7[0],p6[1],0),App.Vector(0,0,1),r),(math.pi/2),(math.pi)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p7[0]),p7[1],0),App.Vector(p8[0],p8[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p8[0]),p8[1],0),App.Vector(p9[0],p9[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p9[0]),p9[1],0),App.Vector(p10[0],p10[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p10[0]),p10[1],0),App.Vector(p11[0],p11[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p11[0]),p11[1],0),App.Vector(p12[0],p12[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p12[0],p13[1],0),App.Vector(0,0,1),r),(0),(math.pi/2)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p13[0]),p13[1],0),App.Vector(p14[0],p14[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p15[0],p14[1],0),App.Vector(0,0,1),r),(1.5*math.pi),(2*math.pi)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p15[0]),p15[1],0),App.Vector(p16[0],p16[1],0)),False)
App.ActiveDocument.HEA200.addGeometry(Part.LineSegment(App.Vector((p16[0]),p16[1],0),App.Vector(p1[0],p1[1],0)),False)

App.activeDocument().recompute()
Gui.getDocument('Unnamed').resetEdit()
ActiveSketch = App.ActiveDocument.getObject('HEA200')
tv = ActiveSketch.ViewObject.TempoVis
if tv:
    tv.restore()
ActiveSketch.ViewObject.TempoVis = None
del(tv)
App.getDocument('Unnamed').recompute()

Gui.activateWorkbench("BIMWorkbench")
