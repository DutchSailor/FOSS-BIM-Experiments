## Webserverdata
DutchGEO_PDOKServerURL = "http://geodata.nationaalgeoregister.nl/locatieserver/v3/free?wt=json&rows=1&q="

DutchGEOCadastreServerRequest1 = "http://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0?service=WFS&version=2.0.0&request=GetFeature&typeName=perceel&bbox="
#For curves of Cadastral Parcels

DutchGEOCadastreServerRequest2 = "http://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0?service=WFS&version=2.0.0&request=GetFeature&typeName=kadastralekaartv4:nummeraanduidingreeks&bbox="
#For 'nummeraanduidingreeks' of Cadastral Parcels

DutchGEOCadastreServerRequest3 = "http://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0?service=WFS&version=2.0.0&request=GetFeature&typeName=kadastralekaartv4:openbareruimtenaam&bbox="
#For 'openbareruimtenaam' of Cadastral Parcels

DutchGEOBAG = "http://geodata.nationaalgeoregister.nl/bag/wfs/v1_1?service=wfs&version=2.0.0&request=GetFeature&typeName=bag:pand&bbox="
#Building Contour of BAG

DutchGEOBAG3D = "http://3dbag.bk.tudelft.nl/data/wfs?&request=GetFeature&typeName=BAG3D:pand3d&outputFormat=GML3&bbox="
#3D Buildings of BAG

DutchGEOLuchtfoto2019WMS = "http://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?&request=GetMap&VERSION=1.3.0&STYLES=&layers=2019_ortho25&width=3000&height=3000&format=image/png&crs=EPSG:28992&bbox="

DutchGEORuimtelijkeplannenBouwvlakServerRequest = "http://afnemers.ruimtelijkeplannen.nl/afnemers/services?&service=WFS&version=1.1.0&request=GetFeature&typeName=app:Bouwvlak&bbox="

xPathCadastre1 = ".//{http://www.opengis.net/gml/3.2}posList"
xPathCadastre2 = ".//{http://www.opengis.net/gml/3.2}pos"
xPathStringsCadastreTextAngle = [".//{http://kadastralekaartv4.geonovum.nl}hoek", ".//{http://kadastralekaartv4.geonovum.nl}tekst"]
xPathRuimtelijkePlannen = ".//{http://www.opengis.net/gml}posList"
xPathStrings3DBag = [".//{3dbag}ground-0.50", ".//{3dbag}roof-0.50"]
xPath3DBag3 = ".//{http://www.opengis.net/gml}posList"
#Xpath for several Web Feature Servers