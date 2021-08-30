# Import Open Street Map

# **************************************************************************
# *                                                                        *
# *  Copyright (c) 2016 microelly <>                                       *
# *  Copyright (c) 2020 Bernd Hahnebach <bernd@bimstatik.org               *
# *  Copyright (c) 2021 Maarten Vroegindeweij(New Interface)               *
# *                                                                        *
# *  This program is free software; you can redistribute it and/or modify  *
# *  it under the terms of the GNU Lesser General Public License (LGPL)    *
# *  as published by the Free Software Foundation; either version 2 of     *
# *  the License, or (at your option) any later version.                   *
# *  for detail see the LICENCE text file.                                 *
# *                                                                        *
# *  This program is distributed in the hope that it will be useful,       *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *  GNU Library General Public License for more details.                  *
# *                                                                        *
# *  You should have received a copy of the GNU Library General Public     *
# *  License along with this program; if not, write to the Free Software   *
# *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *  USA                                                                   *
# *                                                                        *
# **************************************************************************
"""
Import data from OpenStreetMap
"""


from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWebEngineWidgets import QWebEnginePage 
from PySide2.QtCore import QUrl

import os
import FreeCAD

import GIS2BIM
import GIS2BIM_FreeCAD
import GIS2BIM_CRS 


class GISOSM_Dialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(GISOSM_Dialog, self).__init__(parent)
		
		self.sitename = "GIS-Sitedata"
		
		#Get/set parameters for GIS
		self.tempFolderName = "GIStemp/"
		self.lat = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(self.sitename).WGS84_Latitude)
		self.lon = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(self.sitename).WGS84_Longitude)
		self.bboxWidthStart = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(self.sitename).BoundingboxWidth)
		self.bboxHeightStart = str(GIS2BIM_FreeCAD.ArchSiteCreateCheck(self.sitename).BoundingboxHeight)

		#Set Style
		self.setStyleSheet("QWidget {background-color: rgb(68, 68, 68)} QPushButton { background-color: black } QGroupBox {border: 1px solid grey; }") #margin: 2px;
		
		#Download files
		self.URLmap = GIS2BIM.GetWebServerData("HTMLwfs", "Other", "URL")
		#self.filepathBaseMap = GIS2BIM.DownloadURL(GIS2BIM_FreeCAD.CreateTempFolder(self.tempFolderName),self.URLmap,"basemapWFS.html") #Basemap from GIS2BIM Repository for preview
		#self.filepathNewMap = GIS2BIM.DownloadURL(GIS2BIM_FreeCAD.CreateTempFolder(self.tempFolderName),self.URLmap,"mapWFS.html") #Edited Basemap with location and bbox
		self.filepathBaseMap = "C:/Users/mikev/OneDrive/Bureaublad/TEMP/GIStemp/basemapWFS.html"	
		self.filepathNewMap = "C:/Users/mikev/OneDrive/Bureaublad/TEMP/GIStemp/mapWFS.html"	
		self.tempFolderPath = GIS2BIM_FreeCAD.CreateTempFolder(self.tempFolderName)	

		os.remove(self.filepathNewMap)
		BaseMap = open(self.filepathBaseMap,"r")
		BaseMapstr = BaseMap.read()
		Newstr = BaseMapstr.replace("51LAT",str(self.lat))
		Newstr = Newstr.replace("4LONG", str(self.lon))
		Newstr = Newstr.replace("WBBOX",self.bboxWidthStart)
		Newstr = Newstr.replace("HBBOX",self.bboxHeightStart)
		open(self.filepathNewMap, "x")
		f1 = open(self.filepathNewMap, "w")
		f1.write(Newstr)
		f1.close()
		
		#Overall Grid
		grid = QtWidgets.QGridLayout()
		grid.addWidget(self.webViewGroup(), 0, 0, 1, 2)
		grid.addWidget(self.locationGroup(), 3, 0, QtCore.Qt.AlignTop)	
		grid.addLayout(self.buttonGroup(),4,0,1,2)
		grid.setRowStretch(0,2)
		self.setLayout(grid)
		
		self.setWindowTitle("Load 2D Vector Data with WFS(Web Feature Server)")
		self.resize(920, 910)

	def webViewGroup(self):
		groupBox = QtWidgets.QGroupBox("Map")
		groupBox.setStyleSheet("QGroupBox {border: 1px solid grey;}")
		radio1 = QtWidgets.QRadioButton("&Radio button 1")
		radio1.setChecked(True)
		webFrame = QFrame()
		webFrame.setFrameShape(QFrame.StyledPanel)

		vbox = QtWidgets.QVBoxLayout()
	
		groupBox.setLayout(vbox)
		self.webView = QWebEngineView()
		self.webPage = QWebEnginePage()
		self.webPage.load(QUrl(QtCore.QUrl(self.filepathNewMap)))
		self.webView.setObjectName("webView")
		self.webView.setPage(self.webPage)
		self.webView.show()
		vbox.addWidget(self.webView)	
	
		return groupBox

	def locationGroup(self):
		groupBox = QtWidgets.QGroupBox("Location / Boundingbox")
		latLonLab = QtWidgets.QLabel("lat/lon (WGS-84)")
		latLon = QtWidgets.QLabel("lat: " + self.lat + ", lon: " + self.lon)

		bboxWidthLab = QtWidgets.QLabel("Boundingbox Width [m]")
		self.bboxWidth = QtWidgets.QLineEdit()
		self.bboxWidth.setText(self.bboxWidthStart)
		self.bboxWidth.editingFinished.connect(self.onbboxWidth)
		bboxHeightLab = QtWidgets.QLabel("Boundingbox Height [m]")
		self.bboxHeight = QtWidgets.QLineEdit()
		self.bboxHeight.setText(self.bboxHeightStart)
		self.bboxHeight.editingFinished.connect(self.onbboxHeight)	

		grid = QtWidgets.QGridLayout()
		grid.addWidget(latLonLab,0,0)
		grid.addWidget(latLon,0,1)
		grid.addWidget(CRSLab,1,0)
		grid.addWidget(CRSText,1,1)
		grid.addWidget(bboxWidthLab,2,0)
		grid.addWidget(self.bboxWidth,2,1)
		grid.addWidget(bboxHeightLab,3,0)
		grid.addWidget(self.bboxHeight,3,1)

		groupBox.setLayout(grid)
		groupBox.setStyleSheet("QGroupBox {border: 1px solid grey;}")

		return groupBox

	def buttonGroup(self):
		importbtn = QtWidgets.QPushButton("Import")
		importbtn.clicked.connect(self.onImport)
		cancelbtn = QtWidgets.QPushButton("Cancel")	
		cancelbtn.clicked.connect(self.onCancel)

		hbox = QtWidgets.QHBoxLayout()
		hbox.addWidget(importbtn)
		hbox.addWidget(cancelbtn)
				
		return hbox

	def onbboxWidth(self):
		JS2 = open(self.filepathJSUpdate,"r")
		JS2 = JS2.read()
		JS2 = JS2.replace("WBBOX", self.bboxWidth.text())
		JS2 = JS2.replace("HBBOX", self.bboxHeight.text())
		self.webPage.runJavaScript(JS2) # update bboxWidth in mapview
		self.testWFS()

	def onbboxHeight(self):
		JS3 = open(self.filepathJSUpdate,"r")
		JS3 = JS3.read()
		JS3 = JS3.replace("WBBOX", self.bboxWidth.text())
		JS3 = JS3.replace("HBBOX", self.bboxHeight.text())
		self.webPage.runJavaScript(JS3) # update bboxHeight in mapview
		self.testWFS()
	
	def onImport(self):
		self.bboxString = GIS2BIM.CreateBoundingBox(float(GIS2BIM_FreeCAD.ArchSiteCreateCheck(self.sitename).CRS_x),float(GIS2BIM_FreeCAD.ArchSiteCreateCheck(self.sitename).CRS_y),float(self.bboxWidth.text()),float(self.bboxHeight.text()),2)
		url = self.request.text()
		
		xpathstr = self.xPathStr.text()
		closedValue = self.clsPolygon.isChecked()
		makeFaceValue = self.clsCreateFace.isChecked()
		drawStyle = str(self.linePattern.currentText())  
		Curves = GIS2BIM_FreeCAD.CurvesFromWFS(url,self.bboxString,xpathstr,-float(self.X),-float(self.Y),1000,3,closedValue,makeFaceValue,drawStyle,(0.7,0.0,0.0))
		GIS2BIM_FreeCAD.CreateLayer(self.groupName.text())
		FreeCAD.activeDocument().getObject(self.groupName.text()).addObjects(Curves)
		FreeCAD.ActiveDocument.recompute()
		self.close()

	def onCancel(self):
		self.close()

form = GISWFS_Dialog()
form.exec_()


# -------------------------------------------------
# -- osm map importer gui
# --
# -- microelly 2016 v 0.4
# -- Bernd Hahnebach <bernd@bimstatik.org> 2020
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------
"""gui for import data from openstreetmap"""


import WebGui
from PySide import QtGui

# import FreeCAD
# import FreeCADGui

from freecad.trails.geomatics.geoimport import miki
from freecad.trails.geomatics.geoimport.import_osm import import_osm2
from freecad.trails.geomatics.geoimport.say import say


# the gui backend
class MyApp(object):
    """execution layer of the Gui"""

    def import_osm(self, lat, lon, bk, progressbar, status, elevation):
        """
        import the osm data by the use of import_osm module
        """
        has_finished = import_osm2(
            lat,
            lon,
            bk,
            progressbar,
            status,
            elevation
        )
        return has_finished

    def run(self, lat, lon):
        """
        run(self,lat,lon) imports area
        with center coordinates latitude lat, longitude lon
        """
        s = self.root.ids["s"].value()
        key = "%0.7f" % (lat) + "," + "%0.7f" % (lon)
        self.root.ids["bl"].setText(key)
        self.import_osm(
            lat,
            lon,
            float(s)/10,
            self.root.ids["progb"],
            self.root.ids["status"],
            False
        )

    def run_alex(self):
        """imports Berlin Aleancderplatz"""
        self.run(52.52128, lon=13.41646)

    def run_paris(self):
        """imports Paris"""
        self.run(48.85167, 2.33669)

    def run_tokyo(self):
        """imports Tokyo near tower"""
        self.run(35.65905, 139.74991)

    def run_spandau(self):
        """imports Berlin Spandau"""
        self.run(52.508, 13.18)

    def run_co2(self):
        """imports Coburg University and School"""
        self.run(50.2631171, 10.9483)

    def run_sternwarte(self):
        """imports Sonneberg Neufang observatorium"""
        self.run(50.3736049, 11.191643)

    def showHelpBox(self):

        msg = QtGui.QMessageBox()
        msg.setText("<b>Help</b>")
        msg.setInformativeText(
            "Import_osm map dialogue box can also accept links "
            "from following sites in addition to "
            "(latitude, longitude)<ul><li>OpenStreetMap</li><br>"
            "e.g. https://www.openstreetmap.org/#map=15/30.8611/75.8610<br><li>Google Maps</li><br>"
            "e.g. https://www.google.co.in/maps/@30.8611,75.8610,5z<br><li>Bing Map</li><br>"
            "e.g. https://www.bing.com/maps?osid=339f4dc6-92ea-4f25-b25c-f98d8ef9bc45&cp=30.8611~75.8610&lvl=17&v=2&sV=2&form=S00027<br><li>Here Map</li><br>"
            "e.g. https://wego.here.com/?map=30.8611,75.8610,15,normal<br><li>(latitude,longitude)</li><br>"
            "e.g. 30.8611,75.8610</ul><br>"
            "If in any case, the latitude & longitudes are estimated incorrectly, "
            "you can use different separators in separator box "
            "or can put latitude & longitude directly into their respective boxes."
        )
        msg.exec_()

    def showHelpBoxY(self):
        # self.run_sternwarte()
        say("showHelpBox called")

    def getSeparator(self):
        bl = self.root.ids["bl"].text()
        if bl.find("openstreetmap.org") != -1:
            self.root.ids["sep"].setText("/")
        elif bl.find("google.co") != -1:
            self.root.ids["sep"].setText("@|,")
        elif bl.find("bing.com") != -1:
            self.root.ids["sep"].setText("=|~|&")
        elif bl.find("wego.here.com") != -1:
            self.root.ids["sep"].setText("=|,")
        elif bl.find(",") != -1:
            self.root.ids["sep"].setText(",")
        elif bl.find(":") != -1:
            self.root.ids["sep"].setText(":")
        elif bl.find("/") != -1:
            self.root.ids["sep"].setText("/")

    def getCoordinate(self):
        sep = self.root.ids["sep"].text()
        bl = self.root.ids["bl"].text()
        import re
        spli = re.split(sep, bl)
        init_flag = "0"
        flag = init_flag
        for x in spli:
            try:
                float(x)
                if x.find(".") != -1:
                    if flag == "0":
                        self.root.ids["lat"].setText(x)
                        flag = "1"
                    elif flag == "1":
                        self.root.ids["long"].setText(x)
                        flag = "2"
            except Exception:
                flag = init_flag

    def swap(self):
        tmp1 = self.root.ids["lat"].text()
        tmp2 = self.root.ids["long"].text()
        self.root.ids["long"].setText(tmp1)
        self.root.ids["lat"].setText(tmp2)

    def downloadData(self):
        """download data from osm"""
        button = self.root.ids["runbl1"]
        button.hide()
        br = self.root.ids["running"]
        br.show()

        bl_disp = self.root.ids["lat"].text()
        lat = float(bl_disp)
        bl_disp = self.root.ids["long"].text()
        lon = float(bl_disp)

        s = self.root.ids["s"].value()
        elevation = self.root.ids["elevation"].isChecked()

        rc = self.import_osm(
            float(lat),
            float(lon),
            float(s)/10,
            self.root.ids["progb"],
            self.root.ids["status"],
            elevation
        )
        if not rc:
            button = self.root.ids["runbl2"]
            button.show()
        else:
            button = self.root.ids["runbl1"]
            button.show()
        br.hide()

    def applyData(self):
        """apply downloaded or cached data to create the FreeCAD models"""
        button = self.root.ids["runbl2"]
        button.hide()
        br = self.root.ids["running"]
        br.show()

        bl_disp = self.root.ids["lat"].text()
        lat = float(bl_disp)
        bl_disp = self.root.ids["long"].text()
        lon = float(bl_disp)

        s = self.root.ids["s"].value()
        elevation = self.root.ids["elevation"].isChecked()

        self.import_osm(
            float(lat),
            float(lon),
            float(s)/10,
            self.root.ids["progb"],
            self.root.ids["status"],
            elevation
        )
        button = self.root.ids["runbl1"]
        button.show()
        br.hide()

    def showMap(self):
        """
        open a webbrowser window and display
        the openstreetmap presentation of the area
        """

        bl_disp = self.root.ids["lat"].text()
        lat = float(bl_disp)
        bl_disp = self.root.ids["long"].text()
        lon = float(bl_disp)

        # s = self.root.ids["s"].value()
        WebGui.openBrowser(
            "http://www.openstreetmap.org/#map=16/{}/{}".format(lat, lon)
        )

    def showDistanceOnLabel(self):
        distance = self.root.ids["s"].value()
        showDistanceLabel = self.root.ids["showDistanceLabel"]
        showDistanceLabel.setText(
            "Distance is {} km.".format(float(distance)/10)
        )


# the gui startup
def mydialog():
    """ starts the gui dialog """
    print("OSM gui startup")
    app = MyApp()

    my_miki = miki.Miki()
    my_miki.app = app
    app.root = my_miki

    from .miki_import_osm import s6
    my_miki.parse2(s6)
    my_miki.run(s6)
    return my_miki


def importOSM():
    mydialog()


"""
#-----------------
# verarbeiten

import xml.etree.ElementTree as ET

fn="/home/thomas/.FreeCAD//geodat3/50.340722-11.232647-0.015"
#tree = ET.parse(fn)

data_as_string=''<?xml version="1.0"?><data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
''

root = ET.fromstring(data_as_string)


for element in tree.getiterator("node"):
    print(element.attrib)


root = tree.getroot()
ET.dump(root)

for elem in root:
    print (elem.tag,elem.attrib)
#----------------
"""
