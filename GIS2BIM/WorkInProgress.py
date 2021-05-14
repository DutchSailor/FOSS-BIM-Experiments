
#import statements
import sys
sys.path.insert(1, 'C:/Users/mikev/OneDrive/Documenten/GitHub/FOSS-BIM-Experiments/GIS2BIM')
import urllib
import urllib.request
import json
import xml.etree.ElementTree as ET

#Common functions
def GetWebServerData(servertitle, category, parameter):
	Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/GIS2BIM_Data.json"
	url = urllib.request.urlopen(Serverlocation)
	data = json.loads(url.read())['GIS2BIMserversRequests'][category]
	test = []
	for i in data:
		test.append(i["title"])
	result = data[test.index(servertitle)][parameter]
	return result

def GIS2BIM_NominatimAPI(streetname, housenumber, city, country):
    webRequestPart1 = GIS2BIM_NominatimAPIwebRequestPart1
    webRequestPart2 = "%20"
    webRequestLastPart = GIS2BIM_NominatimAPIwebRequestLastPart
    myrequestURL = webRequestPart1 + city + webRequestPart2 + streetname + webRequestPart2 + housenumber + webRequestPart2 + country + webRequestLastPart
    urlFile = urllib.request.urlopen(myrequestURL)
    tree = ET.parse(urlFile)
    return myrequestURL


def GIS2BIM_TransformCRS_epsg(SourceCRS, TargetCRS, X, Y):
    # transform coordinates between different Coordinate Reference Systems using EPSG-server
	SourceCRS = str(SourceCRS)
	TargetCRS = str(TargetCRS)
	X = str(X)
	Y = str(Y)
	requestURL = "http://epsg.io/trans?" + "&s_srs=" + SourceCRS + "&t_srs=" + TargetCRS + "&x=" + X + "&y=" + Y + "&format=json&trans=1&callback=jsonpFunction"
	return requestURL


test = GIS2BIM_TransformCRS_epsg(4326, 28992, 104000, 450000)

GIS2BIM_NominatimAPI

#url = urllib.request.urlopen(test)
#data = json.loads(url.read())
#test = []
#for i in data:
#	test.append(i["title"])
#result = data[test.index(servertitle)][parameter]

print(test)