#import os, sys
#from PySide2.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
#from PySide2.QtWebEngineWidgets import QWebEngineView
#from PySide2.QtCore import QUrl


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class MainWindow(QMainWindow):
    
    
    def __init__(self, parent=None):
        
        super(MainWindow, self).__init__(parent)
        
        self.esaskyBrowserWidget = ESASkyBrowser(self)
        self.controlWidget = ControlBox(self)
        
        _widget = QWidget()
        _layout = QHBoxLayout(_widget)
        
        _layout.addWidget(self.controlWidget)
        _layout.addWidget(self.esaskyBrowserWidget)
        
        self.setCentralWidget(_widget)
        
    def changeFov(self, fovDegrees):
        self.esaskyBrowserWidget.getESASky().page().runJavaScript("window.postMessage({event: 'setFov', content:{fov: "+fovDegrees+"}})")


    def getAvailableHiPS(self, wavelength=''):
        print ('wavelength='+str(wavelength))
        self.esaskyBrowserWidget.getESASky().page().runJavaScript("window.postMessage({event: 'getAvailableHiPS', content:{wavelength: ''}})", self.printJSReturnValues )
        
    def getCataloguesCount(self):
        self.esaskyBrowserWidget.getESASky().page().runJavaScript("window.postMessage({event: 'getCataloguesCount'})", self.printJSReturnValues )
        
      
    def printJSReturnValues(self, jsValues):
        print('printJSReturnValues')
        print(jsValues)  

    
        

class ESASkyBrowser(QWidget):
    
    def __init__(self, parent):
        super(ESASkyBrowser, self).__init__(parent)
        self.__controls()
        self.__layout()

    def __controls(self):
        self.browser = QWebEngineView()
        self.browser.load(QUrl("https://sky.esa.int"))
        self.browser.loadFinished.connect(self.onLoadFinished)

    def __layout(self):
        containerBox = QHBoxLayout()
        containerBox.addWidget(self.browser)
        self.setLayout(containerBox)


    def getESASky(self):
        return self.browser

    def onLoadFinished(self, ok):
        if ok:
            self.browser.page().runJavaScript("window.postMessage({event: 'setFov', content:{fov: 10.0}})")

    def ready(self, returnValue):
        print(returnValue)


    

class ControlBox(QWidget):
    
    def __init__(self, parent):
        super(ControlBox, self).__init__(parent)
        
        self.parentWindow = parent
        self.__layout()
        
    def __layout(self):
        
        # FoV box
        fovLabel = QLabel('FoV in degrees: ', self)
        self.fovInputText = QLineEdit(self)
        self.fovInputText.setPlaceholderText('20.4')
        self.fovInputText.setMinimumWidth(1)
        fovButton = QPushButton("set FoV")
        fovButton.clicked.connect(self.changeFov)
        fovButton.show()
        
        fovBoxWidget = QWidget()
        self.hFovBoxLayout = QHBoxLayout()
        self.hFovBoxLayout.addWidget(fovLabel)
        self.hFovBoxLayout.addWidget(self.fovInputText)
        self.hFovBoxLayout.addWidget(fovButton)
        fovBoxWidget.setLayout(self.hFovBoxLayout)
        
        
        # Get available HiPS
        hipsListButton = QPushButton("Get HiPS list")
        hipsListButton.clicked.connect(self.getAvailableHiPS)
        hipsListButton.show()
        
        # Get catalogues count
        cataloguesCountButton = QPushButton("Get Catalogues count")
        cataloguesCountButton.clicked.connect(self.getCataloguesCount)
        cataloguesCountButton.show()
        
        
        controlBoxWidget = QWidget()
        self.vControlBoxLayout = QVBoxLayout()
        self.vControlBoxLayout.addWidget(fovBoxWidget)
        self.vControlBoxLayout.addWidget(hipsListButton)
        self.vControlBoxLayout.addWidget(cataloguesCountButton)
        
        controlBoxWidget.setLayout(self.vControlBoxLayout)
        

        self.setLayout(self.vControlBoxLayout)
    
    def changeFov(self):
        print ('Clicked on changeFov')
        self.parentWindow.changeFov(self.fovInputText.text())

    def getAvailableHiPS(self, wavelength=''):
        print ('Clicked on getAvailableHiPS')
        print ('wavelength='+str(wavelength))
        self.parentWindow.getAvailableHiPS(wavelength)
        
    def getCataloguesCount(self):
        print ('Clicked on getCataloguesCount')
        self.parentWindow.getCataloguesCount()
        

    def ready(self, returnValue):
        print(returnValue)
        
        
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())