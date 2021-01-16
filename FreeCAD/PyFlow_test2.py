import sys
sys.path.append("C:/FreeCAD_0.19/bin/")
import FreeCAD

'''import image in FreeCAD'''
Doc = FreeCAD.ActiveDocument
#Doc.addObject('Image::ImagePlane', 'ImagePlane')
#Doc.ImagePlane.ImageFile = fileLocation
#Doc.ImagePlane.XSize = width
#Doc.ImagePlane.YSize = height
# Doc.ImagePlane.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0.000000,0.000000,0.000000,1.000000))
#Doc = FreeCAD.ActiveDocument
print(Doc)