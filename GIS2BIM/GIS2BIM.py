## GIS2BIM Library

import urllib
import urllib.request
import xml.etree.ElementTree as ET
import json
import math
import sys
import requests
import re
import os
from PySide2 import QtCore, QtWidgets, QtGui

#Common functions
def GetWebServerData(servertitle, category, parameter):
	#Get webserverdata from github repository of GIS2BIM(up to date list of GIS-servers & requests)
	Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/GIS2BIM_Data.json"
	import urllib.request, json
	url = urllib.request.urlopen(Serverlocation)
	data = json.loads(url.read())['GIS2BIMserversRequests'][category]
	test = []
	for i in data:
		test.append(i["title"])
	result = data[test.index(servertitle)][parameter]
	return result

def DownloadURL(folder,url,filename):
	#Download a file to a folder from a given url
	url = url
	path = folder + filename
	urllib.request.urlretrieve(url,path)
	return path
	
def GetDataFiles(folder):
	Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/datafiles/map.html"
	import urllib.request, json
	url = urllib.request.urlopen(Serverlocation)
	data = json.loads(url.read())['GIS2BIMserversRequests'][category]
	test = []
	for i in data:
		test.append(i["title"])
	result = data[test.index(servertitle)][parameter]
	return result


#GIS2BIM functions

def checkIfCoordIsInsideBoundingBox(coord, bounding_box):
	#check if coordinate is inside rectangle boundingbox
    min_x = bounding_box[0] - (bounding_box[2] / 2)
    min_y = bounding_box[1] - (bounding_box[2] / 2)
    max_x = bounding_box[0] + (bounding_box[2] / 2)
    max_y = bounding_box[1] + (bounding_box[2] / 2)

    if min_x <= float(coord[0]) <= max_x and min_y <= float(coord[1]) <= max_y:
        return True
    else:
        return False
		
def TransformCRS_epsg(SourceCRS, TargetCRS, X, Y):
    # transform coordinates between different Coordinate Reference Systems using EPSG-server
    X = str(X)
    Y = str(Y)
    requestURL = "https://epsg.io/trans?" + "&s_srs=" + SourceCRS + "&t_srs=" + TargetCRS + "&x=" + X + "&y=" + Y + "&format=json"
    rqst = requests.get(requestURL).content
    data = json.loads(rqst)
    X = data["x"]
    Y = data["y"]
    return X,Y

def GML_poslistData(tree, xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
#group X and Y Coordinates of polylines
    posLists = tree.findall(xPathString)
    xyPosList = []
    for posList in posLists:
        dataPosList = posList.text
        coordSplit = dataPosList.split()
        x = 0
        coordSplitXY = []
        for j in range(0, int(len(coordSplit) / XYZCountDimensions)):
            xy_coord = (round((float(coordSplit[x])+dx)*scale,DecimalNumbers), round((float(coordSplit[x+1])+dy)*scale,DecimalNumbers))
            coordSplitXY.append(xy_coord)
            x +=XYZCountDimensions
        xyPosList.append(coordSplitXY)
    return xyPosList

def CreateBoundingBox(CoordinateX,CoordinateY,BoxWidth,BoxHeight,DecimalNumbers):
#Create Boundingboxstring for use in webrequests.
    XLeft = round(CoordinateX-0.5*BoxWidth,DecimalNumbers)
    XRight = round(CoordinateX+0.5*BoxWidth,DecimalNumbers)
    YBottom = round(CoordinateY-0.5*BoxHeight,DecimalNumbers)
    YTop = round(CoordinateY+0.5*BoxHeight,DecimalNumbers)
    boundingBoxString = str(XLeft) + "," + str(YBottom) + "," + str(XRight) + "," + str(YTop)
    return boundingBoxString

def PointsFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
# group X and Y Coordinates
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = GML_poslistData(tree,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    return xyPosList

def DataFromWFS(serverName,boundingBoxString,xPathStringCoord,xPathStrings,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
# group textdata from WFS
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = GML_poslistData(tree,xPathStringCoord,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    xPathResults = []
    for xPathString in xPathStrings:
        a = tree.findall(xPathString)
        xPathResulttemp2 = []
        for xPathResult in a:
            xPathResulttemp2.append(xPathResult.text)
        xPathResults.append(xPathResulttemp2)
    xPathResults.insert(0,xyPosList)
    return xPathResults

def WMSRequest(serverName,boundingBoxString,fileLocation):
    # perform a WMS OGC webrequest( Web Map Service). This is loading images.
    myrequestURL = serverName + boundingBoxString
    resource = urllib.request.urlopen(myrequestURL)
    output1 = open(fileLocation, "wb")
    output1.write(resource.read())
    output1.close()
    return fileLocation, resource, myrequestURL

def MortonCode(X,Y,Xmod,Ymod,TileDimension):
	# convert a x and y coordinate to a mortoncode
	x = bin(int(math.floor(((X - Xmod)/TileDimension))))
	y = bin(int(math.floor(((Y - Ymod)/TileDimension))))
	x = str(x[2:])
	y = str(y[2:])
	res = "".join(i + j for i, j in zip(y, x))
	z=(res)
	z = int(z, 2)
	return z

def GIS2BIM_NominatimAPI(inputlist):
    #get lat/lon via an adress using Nominatim API
	URLpart1 = "https://nominatim.openstreetmap.org/search/"
	URLpart2 = "%20".join(inputlist)
	URLpart3 = "?format=xml&addressdetails=1&limit=1&polygon_svg=1"

	URL = URLpart1 + URLpart2 + URLpart3

	req = urllib.request.Request(URL)
	resp = urllib.request.urlopen(req)
	content = resp.read().decode('utf8')

	lst = re.split('lat=| lon=| display_name=',content)
	lat = lst[1][1:-1]
	lon = lst[2][1:-1]
	
	return lat, lon

class GeoLocation:
    '''

#    Class representing a coordinate on a sphere, most likely Earth.
#    This class is based from the code smaple in this paper:
#        http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
#    The owner of that website, Jan Philip Matuschek, is the full owner of
#    his intellectual property. This class is simply a Python port of his very
#    useful Java code. All code written by Jan Philip Matuschek and ported by me
#    (which is all of this class) is owned by Jan Philip Matuschek.
#    '''

    MIN_LAT = math.radians(-90)
    MAX_LAT = math.radians(90)
    MIN_LON = math.radians(-180)
    MAX_LON = math.radians(180)
    EARTH_RADIUS = 6378.1  # kilometers

    @classmethod
    def from_degrees(cls, deg_lat, deg_lon):
        rad_lat = math.radians(deg_lat)
        rad_lon = math.radians(deg_lon)
        return GeoLocation(rad_lat, rad_lon, deg_lat, deg_lon)

    @classmethod
    def from_radians(cls, rad_lat, rad_lon):
        deg_lat = math.degrees(rad_lat)
        deg_lon = math.degrees(rad_lon)
        return GeoLocation(rad_lat, rad_lon, deg_lat, deg_lon)

    def __init__(
            self,
            rad_lat,
            rad_lon,
            deg_lat,
            deg_lon
    ):
        self.rad_lat = float(rad_lat)
        self.rad_lon = float(rad_lon)
        self.deg_lat = float(deg_lat)
        self.deg_lon = float(deg_lon)
        self._check_bounds()

    def __str__(self):
        degree_sign = u'\N{DEGREE SIGN}'
        return ("{0:.20f}, {1:.20f}").format(
            self.deg_lat, self.deg_lon, self.rad_lat, self.rad_lon)

    def _check_bounds(self):

        if (self.rad_lat < GeoLocation.MIN_LAT
            or self.rad_lat > GeoLocation.MAX_LAT
            or self.rad_lon < GeoLocation.MIN_LON
            or self.rad_lon > GeoLocation.MAX_LON):
            raise Exception("Illegal arguments")

    def distance_to(self, other, radius=EARTH_RADIUS):

        '''

        Computes the great circle distance between this GeoLocation instance
        and the other.
        '''

        return radius * math.acos(
            math.sin(self.rad_lat) * math.sin(other.rad_lat) +
            math.cos(self.rad_lat) *
            math.cos(other.rad_lat) *
            math.cos(self.rad_lon - other.rad_lon)
        )

    def bounding_locations(self, distance, radius=EARTH_RADIUS):

        '''
        Computes the bounding coordinates of all points on the surface
        of a sphere that has a great circle distance to the point represented
        by this GeoLocation instance that is less or equal to the distance argument.

        Param:
            distance - the distance from the point represented by this GeoLocation
                       instance. Must be measured in the same unit as the radius
                       argument (which is kilometers by default)
            radius   - the radius of the sphere. defaults to Earth's radius.
        Returns a list of two GeoLoations - the SW corner and the NE corner - that
        represents the bounding box.
        '''

        if radius < 0 or distance < 0:
            raise Exception("Illegal arguments")

        # angular distance in radians on a great circle

        rad_dist = distance / radius
        min_lat = self.rad_lat - rad_dist
        max_lat = self.rad_lat + rad_dist

        if min_lat > GeoLocation.MIN_LAT and max_lat < GeoLocation.MAX_LAT:
            delta_lon = math.asin(math.sin(rad_dist) / math.cos(self.rad_lat))
            min_lon = self.rad_lon - delta_lon
            if min_lon < GeoLocation.MIN_LON:
                min_lon += 2 * math.pi
            max_lon = self.rad_lon + delta_lon

            if max_lon > GeoLocation.MAX_LON:
                max_lon -= 2 * math.pi

        # a pole is within the distance
        else:

            min_lat = max(min_lat, GeoLocation.MIN_LAT)
            max_lat = min(max_lat, GeoLocation.MAX_LAT)
            min_lon = GeoLocation.MIN_LON
            max_lon = GeoLocation.MAX_LON

        return [GeoLocation.from_radians(min_lat, min_lon),
                GeoLocation.from_radians(max_lat, max_lon)]

