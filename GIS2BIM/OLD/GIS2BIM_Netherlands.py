from GIS2BIM_Lib import *
import urllib.request, json

#jsonpath = "$.GIS2BIMserversRequests.webserverRequests[?(@.title==NetherlandsPDOKServerURL)].serverrequestprefix"

## Webserverdata NL
NLPDOKServerURL = GetWebServerData('NLPDOKServerURL')
NLPDOKCadastreCadastralParcels = GetWebServerData('NLPDOKCadastreCadastralParcels') #For curves of Cadastral Parcels
NLPDOKCadastreCadastralParcelsNummeraanduiding = GetWebServerData('NLPDOKCadastreCadastralParcelsNummeraanduiding') #For 'nummeraanduidingreeks' of Cadastral Parcels
NLPDOKCadastreOpenbareruimtenaam = GetWebServerData('NLPDOKCadastreOpenbareruimtenaam')#For 'openbareruimtenaam' of Cadastral Parcels
NLPDOKBAGBuildingCountour = GetWebServerData('NLPDOKBAGBuildingCountour')  #Building Contour of BAG
NLTUDelftBAG3DV1 = GetWebServerData('NLTUDelftBAG3DV1')  #3D Buildings of BAG
NLRuimtelijkeplannenBouwvlak = GetWebServerData('NLRuimtelijkeplannenBouwvlak')
NLPDOKLuchtfoto2016 = GetWebServerData('NLPDOKLuchtfoto2016')
NLPDOKLuchtfoto2017 = GetWebServerData('NLPDOKLuchtfoto2017')
NLPDOKLuchtfoto2018 = GetWebServerData('NLPDOKLuchtfoto2018')
NLPDOKLuchtfoto2019 = GetWebServerData('NLPDOKLuchtfoto2019')
NLPDOKLuchtfoto2020 = GetWebServerData('NLPDOKLuchtfoto2020')

## Xpath for several Web Feature Servers
NLPDOKxPathOpenGISposList = GetWebServerData('NLPDOKxPathOpenGISposList')
NLPDOKxPathOpenGISPos = GetWebServerData('NLPDOKxPathOpenGISPos')
NLPDOKxPathStringsCadastreTextAngle = GetWebServerData('NLPDOKxPathStringsCadastreTextAngle')
NLPDOKxPathStringsCadastreTextValue = GetWebServerData('NLPDOKxPathStringsCadastreTextValue')
NLPDOKxPathOpenGISPosList2 = GetWebServerData('NLPDOKxPathOpenGISPosList2')
NLTUDelftxPathString3DBagGround = GetWebServerData('NLTUDelftxPathString3DBagGround')
NLTUDelftxPathString3DBagRoof = GetWebServerData('NLTUDelftxPathString3DBagRoof')

xPathStrings3DBag = [NLTUDelftxPathString3DBagGround, NLTUDelftxPathString3DBagRoof]
xPathStringsCadastreTextAngle = [NLPDOKxPathStringsCadastreTextAngle, NLPDOKxPathStringsCadastreTextValue]

#Country specific

#NL Netherlands
def NL_GetLocationData(PDOKServer,City,Streetname,Housenumber):
# Use PDOK location server to get X & Y data
    requestURL =  PDOKServer + City +"%20and%20" + Streetname + "%20and%20" + Housenumber
    urlFile = urllib.request.urlopen(requestURL)
    jsonList = json.load(urlFile)
    jsonList = jsonList["response"]["docs"]
    jsonList1 = jsonList[0]
    RD = jsonList1['centroide_rd']
    RD = RD.replace("("," ").replace(")"," ")
    RD = RD.split()
    RDx = float(RD[1])
    RDy = float(RD[2])
    result = [RDx,RDy,requestURL]
    return result


#Get Rdx/Rdy
a = NL_GetLocationData("dordrecht","Lange%20Geldersekade","2")
width = 500
height = 500
Rdx = float(a[0])
Rdy = float(a[1])

Rdx = 102857.637
Rdy = 425331.936
Bbox = GIS2BIM_CreateBoundingBox(Rdx,Rdy,width,height,2)

fileLocationWMS = 'C:\\TEMP\\test8.jpg'

# Import Aerialphoto in view
GIS2BIM_WMSRequest(DutchGEOLuchtfoto2019WMS,Bbox,fileLocationWMS)
ImageAerialPhoto = GIS2BIM_FreeCAD_ImportImage(fileLocationWMS,width,height,1000)

#Create 3D Building
curves3DBAG = GIS2BIM_PointsFromWFS(DutchGEOBAG3D,Bbox,xPath3DBag3,-Rdx,-Rdy,1000,3,3)
heightData3DBAG = GIS2BIM_DataFromWFS(DutchGEOBAG3D,Bbox,xPath3DBag3,xPathStrings3DBag,-Rdx,-Rdy,1000,3,3)
BAG3DSolids = GIS2BIM_FreeCAD_3DBuildings(curves3DBAG,heightData3DBAG)

#Create Cadastral Parcels 2D
CadastralParcerCurves = GIS2BIM_FreeCAD_CurvesFromWFS(DutchGEOCadastreServerRequest1,Bbox,xPathCadastre1,-Rdx,-Rdy,1000,3,2,False)

#Create Building outline 2D
BAGBuildingCurves = GIS2BIM_FreeCAD_CurvesFromWFS(DutchGEOBAG,Bbox,xPathCadastre1,-Rdx,-Rdy,1000,3,2,True)

#Create Ruimtelijke plannen outline 2D
RuimtelijkePlannenBouwvlakCurves = GIS2BIM_FreeCAD_CurvesFromWFS(DutchGEORuimtelijkeplannenBouwvlakServerRequest,Bbox,xPathRuimtelijkePlannen,-Rdx,-Rdy,1000,3,2,True)

#Create Textdata Cadastral Parcels
textDataCadastralParcels = GIS2BIM_DataFromWFS(DutchGEOCadastreServerRequest2,Bbox,xPathCadastre2,xPathStringsCadastreTextAngle,-Rdx,-Rdy,1000,3,2)
textDataOpenbareRuimtenaam = GIS2BIM_DataFromWFS(DutchGEOCadastreServerRequest3,Bbox,xPathCadastre2,xPathStringsCadastreTextAngle,-Rdx,-Rdy,1000,3,2)

placeTextCadastralParcels = GIS2BIM_FreeCAD_PlaceText(textDataCadastralParcels,200)
placeTextOpenbareRuimteNaam = GIS2BIM_FreeCAD_PlaceText(textDataOpenbareRuimtenaam,200)

FreeCAD.ActiveDocument.recompute()