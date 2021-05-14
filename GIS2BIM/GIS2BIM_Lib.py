## GIS2BIM Library

#Common functions
def GIS2BIM_GetServerData(servertitle):
	Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/GIS2BIM_Data.json"
	import urllib.request, json
	url = urllib.request.urlopen(Serverlocation)
	data = json.loads(url.read())['GIS2BIMserversRequests']['webserverRequests']
	test = []
	for i in data:
		test.append(i["title"])
	url = data[test.index(servertitle)]['serverrequestprefix']
	return url

#GIS2BIM functions

def GIS2BIM_GML_poslistData(tree, xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
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

def GIS2BIM_CreateBoundingBox(CoordinateX,CoordinateY,BoxWidth,BoxHeight,DecimalNumbers):
#Create Boundingboxstring for use in webrequests.
    XLeft = round(CoordinateX-0.5*BoxWidth,DecimalNumbers)
    XRight = round(CoordinateX+0.5*BoxWidth,DecimalNumbers)
    YBottom = round(CoordinateY-0.5*BoxHeight,DecimalNumbers)
    YTop = round(CoordinateY+0.5*BoxHeight,DecimalNumbers)
    boundingBoxString = str(XLeft) + "," + str(YBottom) + "," + str(XRight) + "," + str(YTop)
    return boundingBoxString

def GIS2BIM_PointsFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
# group X and Y Coordinates
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = GIS2BIM_GML_poslistData(tree,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    return xyPosList

def GIS2BIM_DataFromWFS(serverName,boundingBoxString,xPathStringCoord,xPathStrings,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
# group textdata from WFS
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = GIS2BIM_GML_poslistData(tree,xPathStringCoord,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    xPathResults = []
    for xPathString in xPathStrings:
        a = tree.findall(xPathString)
        xPathResulttemp2 = []
        for xPathResult in a:
            xPathResulttemp2.append(xPathResult.text)
        xPathResults.append(xPathResulttemp2)
    xPathResults.insert(0,xyPosList)
    return xPathResults

def GIS2BIM_WMSRequest(serverName,boundingBoxString,fileLocation):
    # perform a WMS OGC webrequest( Web Map Service). This is loading images.
    myrequestURL = serverName + boundingBoxString
    resource = urllib.request.urlopen(myrequestURL)
    output1 = open(fileLocation, "wb")
    output1.write(resource.read())
    output1.close()
    return fileLocation, resource
	
#Country specific

#NL Netherlands
def GIS2BIM_NL_GetLocationData(PDOKServer,City,Streetname,Housenumber):
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