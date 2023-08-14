import json
import requests
import urllib
import urllib.request
from urllib.request import urlopen


NLPDOKBGTURL1 = "https://api.pdok.nl/lv/bgt/download/v1_0/full/custom"
NLPDOKBGTURL2 = "https://api.pdok.nl"

url = NLPDOKBGTURL1
url2 = NLPDOKBGTURL2

def CreateBoundingBoxPolygon(CoordinateX,CoordinateY,BoxWidth,BoxHeight,DecimalNumbers):
#Create Boundingboxstring for use in webrequests.
    XLeft = round(CoordinateX-0.5*BoxWidth,DecimalNumbers)
    XRight = round(CoordinateX+0.5*BoxWidth,DecimalNumbers)
    YBottom = round(CoordinateY-0.5*BoxHeight,DecimalNumbers)
    YTop = round(CoordinateY+0.5*BoxHeight,DecimalNumbers)
    boundingBoxStringPolygon = "(" + str(XLeft) + ' ' + str(YTop) + ',' + str(XRight) + ' ' + str(YTop) + ',' + str(XRight) + ' ' + str(YBottom) + ',' + str(XLeft) + ' ' + str(YBottom) + ',' + str(XLeft) + ' ' + str(YTop) + ')'
    return boundingBoxStringPolygon

polygonString = CreateBoundingBoxPolygon(100000,500000,500,500,0)

##Define data
qryPart1 = '{"featuretypes":['
qryPart2 = '"bak","begroeidterreindeel","bord","buurt","functioneelgebied","gebouwinstallatie","installatie","kast","kunstwerkdeel","mast","onbegroeidterreindeel","ondersteunendwaterdeel","ondersteunendwegdeel","ongeclassificeerdobject","openbareruimte","openbareruimtelabel","overbruggingsdeel","overigbouwwerk","overigescheiding","paal","pand","put","scheiding","sensor","spoor","stadsdeel","straatmeubilair","tunneldeel","vegetatieobject","waterdeel","waterinrichtingselement","waterschap","weginrichtingselement","wijk","wegdeel"'
qryPart3 = '],"format":"gmllight","geofilter":"POLYGON('
qryPart4 = polygonString
qryPart5 = ')"}'

data = qryPart1 + qryPart2 + qryPart3 + qryPart4 + qryPart5
dataquery = data

headers = requests.structures.CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["Content-Type"] = "application/json"

#resp = requests.post(url, headers=headers, data=data)

#jsondata = json.loads(resp.text)

custom_headers = {
    "Content-Type": "application/json",
    "accept": "application/json"}

from urllib.request import Request

req = Request(
    url,
    json.dumps(dataquery).encode('ascii'),
    custom_headers)

test = urlopen(req)

print(test)
#with urlopen(req) as response:
#    json_response = json.load(response)

