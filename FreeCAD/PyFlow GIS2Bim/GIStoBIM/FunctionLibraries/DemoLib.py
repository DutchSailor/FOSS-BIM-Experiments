from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE

import sys
sys.path.insert(1, 'C:/Users/mikev/OneDrive/Documenten/GitHub/GIS2BIM')
import GIS2BIM_Lib
from array import array

class DemoLib(FunctionLibraryBase):
    '''doc string for DemoLib'''

    def __init__(self, packageName):
        super(DemoLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', "empty"), meta={NodeMeta.CATEGORY: 'Coordinates', NodeMeta.KEYWORDS: []})
    def GIS2BIM_CreateBoundingBox(CoordinateX=('FloatPin', 0.0), CoordinateY=('FloatPin', 0.0), BoxWidth=('FloatPin', 0.0), BoxHeight=('FloatPin', 0.0), DecimalNumbers=('IntPin', 2)):
        '''Create boundingboxstring for webrequests based on coordinates and dimensions.'''
        boundingBoxString = GIS2BIM_Lib.GIS2BIM_CreateBoundingBox(CoordinateX,CoordinateY,BoxWidth,BoxHeight,DecimalNumbers)
        return boundingBoxString
		
    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin',"") , meta={NodeMeta.CATEGORY: 'GIS-Netherlands', NodeMeta.KEYWORDS: []})
    def GIS2BIM_GetLocationDataNetherlands(City=('StringPin', "Dordrecht"), StreetName=('StringPin', "LangeGeldersekade"), HouseNumber=('StringPin', "2")):
        '''Gives locationdata based on an address in the Netherlands.'''
        Result = GIS2BIM_Lib.GIS2BIM_GetLocationDataNetherlands(City,StreetName,HouseNumber)
        return Result

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', "empty"), meta={NodeMeta.CATEGORY: 'WMS/WFS Webrequests', NodeMeta.KEYWORDS: []})
    def GIS2BIM_WMSRequest(serverName=('StringPin', ""), boundingBoxString=('StringPin', ""), fileLocation=('StringPin', "2")):
        '''a webrequest based on WMS-protocol(Web Map Service'''
        Result = GIS2BIM_Lib.GIS2BIM_WMSRequest(serverName,boundingBoxString,fileLocation)
        return Result

    @staticmethod
    @IMPLEMENT_NODE(returns=('StringPin', "empty"), meta={NodeMeta.CATEGORY: 'Test', NodeMeta.KEYWORDS: []})
    def GIS2BIM_Test(X=('AnyPin',"")):
        '''test'''
        Z = GIS2BIM_Lib.DutchGEOLuchtfoto2019WMS
        return Z