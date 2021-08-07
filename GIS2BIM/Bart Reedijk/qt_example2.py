import sys
import os

from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel

class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, parent=None):
        super(WebEnginePage, self).__init__(parent)
        # setup channel
        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject('backend', self)
        self.setWebChannel(self.channel)

    @QtCore.Slot(str)
    def sendLatLng(self, output):
        print(output)

            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    filename = QtCore.QDir.current().filePath("map-new.html")
    url = QtCore.QUrl.fromLocalFile(filename)
    page = WebEnginePage()
    view = QtWebEngineWidgets.QWebEngineView()
    page.load(url)
    view.setPage(page)
    view.resize(1000, 800)
    view.show()
    sys.exit(app.exec_())