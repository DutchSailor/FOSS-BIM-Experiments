## snapGIS Library

def snapGIS_GML_poslistData(tree, xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
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

def snapGIS_CreateBoundingBox(CoordinateX,CoordinateY,BoxWidth,BoxHeight,DecimalNumbers):
#Create Boundingboxstring for use in webrequests.
    XLeft = round(CoordinateX-0.5*BoxWidth,DecimalNumbers)
    XRight = round(CoordinateX+0.5*BoxWidth,DecimalNumbers)
    YBottom = round(CoordinateY-0.5*BoxHeight,DecimalNumbers)
    YTop = round(CoordinateY+0.5*BoxHeight,DecimalNumbers)
    boundingBoxString = str(XLeft) + "," + str(YBottom) + "," + str(XRight) + "," + str(YTop)
    return boundingBoxString

def snapGIS_GetLocationDataNetherlands(City,Streetname,Housenumber):
# Use PDOK location server to get X & Y data
    PDOKServer = DutchGEO_PDOKServerURL
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

def snapGIS_PointsFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
# group X and Y Coordinates
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = snapGIS_GML_poslistData(tree,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    return xyPosList

def snapGIS_DataFromWFS(serverName,boundingBoxString,xPathStringCoord,xPathStrings,dx,dy,scale,DecimalNumbers,XYZCountDimensions):
# group textdata from WFS
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = snapGIS_GML_poslistData(tree,xPathStringCoord,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    xPathResults = []
    for xPathString in xPathStrings:
        a = tree.findall(xPathString)
        xPathResulttemp2 = []
        for xPathResult in a:
            xPathResulttemp2.append(xPathResult.text)
        xPathResults.append(xPathResulttemp2)
    xPathResults.insert(0,xyPosList)
    return xPathResults

def snapGIS_WMSRequest(serverName,boundingBoxString,fileLocation):
    # perform a WMS OGC webrequest( Web Map Service). This is loading images.
    myrequestURL = serverName + boundingBoxString
    resource = urllib.request.urlopen(myrequestURL)
    output1 = open(fileLocation, "wb")
    output1.write(resource.read())
    output1.close()
    return fileLocation, resource

## snapGIS within FreeCAD

#import snapGIS_Lib
import urllib.request
import urllib
import xml.etree.ElementTree as ET
import json
import Draft
import Part

def snapGIS_FreeCAD_ImportImage(fileLocation,width,height,scale):
    App.activeDocument().addObject('Image::ImagePlane','ImagePlane')
    App.activeDocument().ImagePlane.ImageFile = fileLocation
    App.activeDocument().ImagePlane.XSize = width*scale
    App.activeDocument().ImagePlane.YSize = height*scale
    App.activeDocument().ImagePlane.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))

def snapGIS_FreeCAD_3DBuildings(curves3DBAG,heightData3DBAG):
    for i,j,k in zip(curves3DBAG,heightData3DBAG[1],heightData3DBAG[2]):
        pointlist = []
        for curve in i:
            pointlist.append(FreeCAD.Vector(curve[0], curve[1], float(j)*1000))
        a = Part.makePolygon(pointlist)
        face = Part.Face(a)
        solid = face.extrude(FreeCAD.Vector(0, 0, float(k) * 1000))
        Part.show(solid)
    return solid

def snapGIS_FreeCAD_CurvesFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions,closedValue,DrawStyle,LineColor):
    curves = snapGIS_PointsFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers,XYZCountDimensions)
    for i in curves:
        pointlist = []
        for j in i:
            pointlist.append(FreeCAD.Vector(j[0], j[1], 0))
        a = Draft.makeWire(pointlist, closed=closedValue)
        a.MakeFace = closedValue
        a.ViewObject.DrawStyle = DrawStyle
        a.ViewObject.LineColor = LineColor
    return a

def snapGIS_FreeCAD_PlaceText(textData,fontSize):
    for i, j, k in zip(textData[0], textData[1], textData[2]):
        ZAxis = FreeCAD.Vector(0, 0, 1)
        p1 = FreeCAD.Vector(i[0][0], i[0][1], 0)
        Place1 = FreeCAD.Placement(p1, FreeCAD.Rotation(ZAxis, -float(j)))
        Text1 = Draft.makeText(k, point=p1)
        Text1.ViewObject.FontSize = fontSize
        Text1.Placement = Place1
    return Text1

# import statements
from PySide import QtGui, QtCore

# UI Class definitions

class snapGIS_Dialog(QtGui.QDialog):
	""""""
	def __init__(self):
		super(snapGIS_Dialog, self).__init__()
		self.initUI()
	def initUI(self):
		self.result = userCancelled
		# create our window
		# define window		xLoc,yLoc,xDim,yDim
		self.setGeometry(250, 250, 400, 450)
		self.setWindowTitle("Load GIS-data")
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		# create some Labels
		self.label1 = QtGui.QLabel("Rdx(EPSG 28992)", self)
		self.label1.move(20, 20)
		#
		self.numericInput1Rdx = QtGui.QLineEdit(self)
		self.numericInput1Rdx.setInputMask("")
		self.numericInput1Rdx.setText("102857.637")
		self.numericInput1Rdx.setFixedWidth(100)
		self.numericInput1Rdx.move(250, 20)
		#
		self.label2 = QtGui.QLabel("Rdy(EPSG 28992)", self)
		self.label2.move(20, 50)
		#
		self.numericInput2Rdy = QtGui.QLineEdit(self)
		self.numericInput2Rdy.setInputMask("")
		self.numericInput2Rdy.setText("425331.936")
		self.numericInput2Rdy.setFixedWidth(100)
		self.numericInput2Rdy.move(250, 50)
		#
		self.label3 = QtGui.QLabel("Boundingbox Width(m)", self)
		self.label3.move(20, 80)
		#
		self.numericInput3Width = QtGui.QLineEdit(self)
		self.numericInput3Width.setInputMask("")
		self.numericInput3Width.setText("500")
		self.numericInput3Width.setFixedWidth(100)
		self.numericInput3Width.move(250, 80)
		#
		self.label4 = QtGui.QLabel("Boundingbox Height(m)", self)
		self.label4.move(20, 110)
		#
		self.numericInput4Height = QtGui.QLineEdit(self)
		self.numericInput4Height.setInputMask("")
		self.numericInput4Height.setText("500")
		self.numericInput4Height.setFixedWidth(100)
		self.numericInput4Height.move(250, 110)
		# checkboxes
		self.checkbox1 = QtGui.QCheckBox("Cadastral Parcels 2D", self)
		self.checkbox1.move(20,140)
		#
		self.checkbox2 = QtGui.QCheckBox("Building Outline 2D", self)
		self.checkbox2.move(20,170)
		#
		self.checkbox3 = QtGui.QCheckBox("3D Buildings", self)
		self.checkbox3.move(20,200)
		#
		self.checkbox4 = QtGui.QCheckBox("2D Aerialphoto", self)
		self.checkbox4.move(20,230)
		#
		self.checkbox5 = QtGui.QCheckBox("GIS 2D Annotation", self)
		self.checkbox5.move(20,260)
		#
		self.checkbox6 = QtGui.QCheckBox("Bestemmingsplan", self)
		self.checkbox6.move(20,290)
		#
		# cancel button
		cancelButton = QtGui.QPushButton('Cancel', self)
		cancelButton.clicked.connect(self.onCancel)
		cancelButton.setAutoDefault(True)
		cancelButton.move(150, 350)
		# OK button
		okButton = QtGui.QPushButton('OK', self)
		okButton.clicked.connect(self.onOk)
		okButton.move(260, 350)
		# now make the window visible
		self.show()
		#
	def onCancel(self):
		self.result			= userCancelled
		self.close()
	def onOk(self):
		self.result			= userOK
		self.close()

# Class definitions

# Function definitions

# Constant definitions
userCancelled		= "Cancelled"
userOK			= "OK"

# code ***********************************************************************************

form = snapGIS_Dialog()
form.exec_()

if form.result==userCancelled:
	pass # steps to handle user clicking Cancel
if form.result==userOK:
	# steps to handle user clicking OK
	Rdx = float(form.numericInput1Rdx.text())
	Rdy = float(form.numericInput2Rdy.text())
	width = float(form.numericInput3Width.text())
	height = float(form.numericInput4Height.text())
	CadastralParcels2D = form.checkbox1.isChecked()
	BuildingOutline2D = form.checkbox2.isChecked()
	Buildings3D = form.checkbox3.isChecked()
	Aerialphoto2D = form.checkbox4.isChecked()
	GIS2DAnnotation = form.checkbox5.isChecked()
	Bestemmingsplan = form.checkbox6.isChecked()

Bbox = snapGIS_CreateBoundingBox(Rdx,Rdy,width,height,2)

fileLocationWMS = 'C:\\TEMP\\test8.jpg'

#Create Cadastral Parcels 2D
if CadastralParcels2D is True:
	CadastralParcelCurves = snapGIS_FreeCAD_CurvesFromWFS(DutchGEOCadastreServerRequest1,Bbox,xPathCadastre1,-Rdx,-Rdy,1000,3,2,False,u"Dashdot",(0.0,0.0,0.0))

#Create Building outline 2D
if BuildingOutline2D is True:
	BAGCurves = snapGIS_FreeCAD_CurvesFromWFS(DutchGEOBAG,Bbox,xPathCadastre1,-Rdx,-Rdy,1000,3,2,True,u"Solid",(0.7,0.0,0.0))

#Create 3D Building
if Buildings3D is True:
	curves3DBAG = snapGIS_PointsFromWFS(DutchGEOBAG3D,Bbox,xPath3DBag3,-Rdx,-Rdy,1000,3,3)
	heightData3DBAG = snapGIS_DataFromWFS(DutchGEOBAG3D,Bbox,xPath3DBag3,xPathStrings3DBag,-Rdx,-Rdy,1000,3,3)
	BAG3DSolids = snapGIS_FreeCAD_3DBuildings(curves3DBAG,heightData3DBAG)

# Import Aerialphoto in view
if Aerialphoto2D is True:
	snapGIS_WMSRequest(DutchGEOLuchtfoto2019WMS,Bbox,fileLocationWMS)
	ImageAerialPhoto = snapGIS_FreeCAD_ImportImage(fileLocationWMS,width,height,1000)

#Create Textdata Cadastral Parcels
if GIS2DAnnotation is True:
	textDataCadastralParcels = snapGIS_DataFromWFS(DutchGEOCadastreServerRequest2,Bbox,xPathCadastre2,xPathStringsCadastreTextAngle,-Rdx,-Rdy,1000,3,2)
	textDataOpenbareRuimtenaam = snapGIS_DataFromWFS(DutchGEOCadastreServerRequest3,Bbox,xPathCadastre2,xPathStringsCadastreTextAngle,-Rdx,-Rdy,1000,3,2)
	placeTextFreeCAD = snapGIS_FreeCAD_PlaceText(textDataCadastralParcels,50)
	placeTextFreeCAD = snapGIS_FreeCAD_PlaceText(textDataOpenbareRuimtenaam,200)

#Create Ruimtelijke plannen outline 2D
if Bestemmingsplan is True:
	RuimtelijkePlannenBouwvlakCurves = snapGIS_FreeCAD_CurvesFromWFS(DutchGEORuimtelijkeplannenBouwvlakServerRequest,Bbox,xPathRuimtelijkePlannen,-Rdx,-Rdy,1000,3,2,False,u"Solid",(0.0,0.0,1.0))

FreeCAD.ActiveDocument.recompute()