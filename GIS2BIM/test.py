import GIS2BIM_FreeCAD
from pivy import coin
global path

class IconViewProviderToFile:                                       # Class ViewProvider create Property view of object
    def __init__( self, obj, icon):
        self.icone = icon
        
    def getIcon(self):                                              # GetIcon
        return self.icone
        
    def attach(self, obj):                                          # Property view of object
        self.modes = []
        self.modes.append("Flat Lines")
        self.modes.append("Shaded")
        self.modes.append("Wireframe")
        self.modes.append("Points")
        obj.addDisplayMode( coin.SoGroup(),"Flat Lines" )           # Display Mode
        obj.addDisplayMode( coin.SoGroup(),"Shaded" )
        obj.addDisplayMode( coin.SoGroup(),"Wireframe" )
        obj.addDisplayMode( coin.SoGroup(),"Points" )
        return self.modes

    def getDisplayModes(self,obj):
        return self.modes

param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")# macro path in FreeCAD preferences
path = param.GetString("MacroPath","") + "/"                        # macro path
path = path.replace("\\","/")                                       # convert the "\" to "/"

#obj = FreeCAD.activeDocument().addObject("App::DocumentObjectGroupPython", "GIS-test7")
#obj = CreateLayer("GIS-test4")


#obj.ViewObject.Proxy.icone = path + "/Icons/ImportWMS.svg"                                   # icon download to file



image h