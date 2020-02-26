import os, sys
from PySide2.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import QUrl
from lib2to3.fixer_util import parenthesize


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
        
        self.hFovBox = QHBoxLayout()
        self.hFovBox.addWidget(fovLabel)
        self.hFovBox.addWidget(self.fovInputText)
        self.hFovBox.addWidget(fovButton)

        self.setLayout(self.hFovBox)
        
    def changeFov(self):
        self.parentWindow.changeFov(self.fovInputText.text())

    def ready(self, returnValue):
        print(returnValue)
        
        
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())