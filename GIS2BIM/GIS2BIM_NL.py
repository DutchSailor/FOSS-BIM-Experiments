import GIS2BIM
#import urllib.request, json

#jsonpath = "$.GIS2BIMserversRequests.webserverRequests[?(@.title==NetherlandsPDOKServerURL)].serverrequestprefix"

## Webserverdata NL
NLPDOKServerURL = GIS2BIM.GetWebServerData('NLPDOKServerURL','webserverRequests','serverrequestprefix')
NLPDOKCadastreCadastralParcels = GIS2BIM.GetWebServerData('NLPDOKCadastreCadastralParcels','webserverRequests','serverrequestprefix') #For curves of Cadastral Parcels
NLPDOKCadastreCadastralParcelsNummeraanduiding = GIS2BIM.GetWebServerData('NLPDOKCadastreCadastralParcelsNummeraanduiding','webserverRequests','serverrequestprefix') #For 'nummeraanduidingreeks' of Cadastral Parcels
NLPDOKCadastreOpenbareruimtenaam = GIS2BIM.GetWebServerData('NLPDOKCadastreOpenbareruimtenaam','webserverRequests','serverrequestprefix')#For 'openbareruimtenaam' of Cadastral Parcels
NLPDOKBAGBuildingCountour = GIS2BIM.GetWebServerData('NLPDOKBAGBuildingCountour','webserverRequests','serverrequestprefix')  #Building Contour of BAG
NLTUDelftBAG3DV1 = GIS2BIM.GetWebServerData('NLTUDelftBAG3DV1','webserverRequests','serverrequestprefix')  #3D Buildings of BAG
NLRuimtelijkeplannenBouwvlak = GIS2BIM.GetWebServerData('NLRuimtelijkeplannenBouwvlak','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2016 = GIS2BIM.GetWebServerData('NLPDOKLuchtfoto2016','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2017 = GIS2BIM.GetWebServerData('NLPDOKLuchtfoto2017','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2018 = GIS2BIM.GetWebServerData('NLPDOKLuchtfoto2018','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2019 = GIS2BIM.GetWebServerData('NLPDOKLuchtfoto2019','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2020 = GIS2BIM.GetWebServerData('NLPDOKLuchtfoto2020','webserverRequests','serverrequestprefix')

## Xpath for several Web Feature Servers
NLPDOKxPathOpenGISposList = GIS2BIM.GetWebServerData('NLPDOKxPathOpenGISposList','Querystrings','querystring')
NLPDOKxPathOpenGISPos = GIS2BIM.GetWebServerData('NLPDOKxPathOpenGISPos','Querystrings','querystring')
NLPDOKxPathStringsCadastreTextAngle = GIS2BIM.GetWebServerData('NLPDOKxPathStringsCadastreTextAngle','Querystrings','querystring')
NLPDOKxPathStringsCadastreTextValue = GIS2BIM.GetWebServerData('NLPDOKxPathStringsCadastreTextValue','Querystrings','querystring')
NLPDOKxPathOpenGISPosList2 = GIS2BIM.GetWebServerData('NLPDOKxPathOpenGISPosList2','Querystrings','querystring')
NLTUDelftxPathString3DBagGround = GIS2BIM.GetWebServerData('NLTUDelftxPathString3DBagGround','Querystrings','querystring')
NLTUDelftxPathString3DBagRoof = GIS2BIM.GetWebServerData('NLTUDelftxPathString3DBagRoof','Querystrings','querystring')

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