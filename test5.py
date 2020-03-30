import sys
from PyQt5.QtCore import pyqtSlot, QUrl, QObject, QJsonValue, QJsonDocument
from PyQt5.QtWidgets import QListWidget, QStackedWidget, QDesktopWidget, QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from panels.outgoing import AbstractWidget, FovBox, CataloguesCount, GoToTargetName, GetAvailableHiPS



class MainWindow(QMainWindow):
    
    
    def __init__(self, parent=None):
        
        super(MainWindow, self).__init__(parent)
        
        self.esaskyBrowserWidget = ESASkyWrapper(self)
        self.controlWidget = ControlBox(self.esaskyBrowserWidget)
        
        _widget = QWidget()
        _layout = QHBoxLayout(_widget)
        
        _layout.addWidget(self.controlWidget, 1)
        _layout.addWidget(self.esaskyBrowserWidget, 2)
        
        self.setCentralWidget(_widget)
        
    def setResult(self, result):
        self.controlWidget.setResultText(result)

class ESASkyWrapper(QWebEngineView):

    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        #url = QUrl.fromLocalFile(r"/Users/fgiordano/Workspace/esaskyQT/index.html")
        import pathlib
        pathlib.Path(__file__).parent.absolute()
        print (pathlib.Path(__file__).parent.absolute())
        path = str(pathlib.Path(__file__).parent.absolute())+'/index.html'
        url = QUrl.fromLocalFile(path)
        self.load(url)

        # setup channel
        self.channel = QWebChannel()
        self.channel.registerObject('backend', self)
        self.page().setWebChannel(self.channel)
        self.show()

        
    @pyqtSlot(str)
    def foo(self, arg1):
        import json
        mydict = json.loads(arg1)
        self.parent.setResult(arg1)
 
class ControlBox(QWidget):
    
    def __init__(self, esaskyWrapper):
        super(ControlBox, self).__init__()
        #super(ControlBox, self).__init__(parent)
        
        #self.parentWindow = parent
        self.esaskyWrapper = esaskyWrapper
        self.__layout()
        
    def __layout(self):
        
        self.esaskyAPIList = QListWidget ()
        self.esaskyAPIList.insertItem (0, 'empty' )
        self.esaskyAPIList.insertItem (1, 'setFov' )
        self.esaskyAPIList.insertItem (2, 'getCataloguesCount' )
        self.esaskyAPIList.insertItem (3, 'goToTargetName' )
        self.esaskyAPIList.insertItem (4, 'getAvailableHiPS' )
        
        
        
        self.esaskyAPIList.currentRowChanged.connect(self.displayWidget)
        
        
        emptyWidget = QWidget()
        fovWidget = FovBox(self.esaskyWrapper)
        catsCountWidget = CataloguesCount(self.esaskyWrapper)
        goToTargetWidget = GoToTargetName(self.esaskyWrapper)
        getAvailableHiPSWidget = GetAvailableHiPS(self.esaskyWrapper)
        
        self.stack = QStackedWidget (self)
        self.stack.addWidget(emptyWidget)
        self.stack.addWidget(fovWidget)
        self.stack.addWidget(catsCountWidget)
        self.stack.addWidget(goToTargetWidget)
        self.stack.addWidget(getAvailableHiPSWidget)
        
        
        self.stack.setCurrentIndex(0)
        
        resultWidget = QWidget()
        resultLabel = QLabel('result', self)
        self.resultText = QLabel('', self)
        self.resultText.setWordWrap(True)
        rLayout = QVBoxLayout()
        rLayout.addWidget(resultLabel)
        rLayout.addWidget(self.resultText)
        resultWidget.setLayout(rLayout)
     
        
        controlBoxWidget = QWidget()
        self.vControlBoxLayout = QVBoxLayout()
        self.vControlBoxLayout.addWidget(self.esaskyAPIList)
        self.vControlBoxLayout.addWidget(self.stack)
        self.vControlBoxLayout.addWidget(resultWidget)
        
        controlBoxWidget.setLayout(self.vControlBoxLayout)
        self.setLayout(self.vControlBoxLayout)

    def displayWidget(self, i):
        self.setResultText('')
        self.stack.setCurrentIndex(i)
        currWidget = self.stack.widget(i)
        try:
            currWidget.directRun()
        except AttributeError:
            print ('attribute not found')
        
        
    def setResultText(self, text):
        self.resultText.setText(text)



if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    view = MainWindow()
    
    desktop = QDesktopWidget()
    width = desktop.width()*0.7;
    height = desktop.height()*0.7;
    view.setFixedSize(width,height);
    view.show()
    app.exec_()
