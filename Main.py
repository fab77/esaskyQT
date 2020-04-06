'''
    File name: Main.py
    Author: Fabrizio Giordano
    Date created: 05/20/2020
    Python Version: 3.7.3
'''

import sys
from PyQt5.QtCore import pyqtSlot, QUrl, QObject, QJsonValue, QJsonDocument
from PyQt5.QtWidgets import QListWidget, QStackedWidget, QDesktopWidget, QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from panels.outgoing import AbstractWidget, FovBox, CataloguesCount, GoToTargetName, GetAvailableHiPS
from PyQt5.Qt import QTableWidget, QTableWidgetItem
from astropy.table import Table
import pathlib

class MainWindow(QMainWindow):
    
    
    def __init__(self, parent=None):
        
        super(MainWindow, self).__init__(parent)
        
        self.esaskyBrowserWidget = ESASkyWrapper(self)
        if showCommands:
            self.controlWidget = ControlBox(self.esaskyBrowserWidget)
        
        _hwidget = QWidget()
        _hlayout = QHBoxLayout()
        _hwidget.setLayout(_hlayout)
        
        self.tableWidget = ResultTable()
        _vlayout = QVBoxLayout()
        _vlayout.addWidget(_hwidget)
        _vlayout.addWidget(self.tableWidget)
        _vwidget = QWidget()
        _vwidget.setLayout(_vlayout)
        
        if showCommands:
            _hlayout.addWidget(self.controlWidget, 1)
            _hlayout.addWidget(self.esaskyBrowserWidget, 2)
        else:
            _hlayout.addWidget(self.esaskyBrowserWidget, 1)
        
        # setup channel
        self.channel = QWebChannel()
        self.channel.registerObject('backend', self)
        self.esaskyBrowserWidget.page().setWebChannel(self.channel)
        
        self.setCentralWidget(_vwidget)
        
        #QObject.connect(a,SIGNAL("testInit"),self.pippo,Qt.QueuedConnection)
        
    def pippo(self):
        return "test"
        
    def setResult(self, result):
        self.controlWidget.getCurrentWidget().prepareTabularOutput(result)
        
    @pyqtSlot(str)
    def foo(self, arg1):
        import json
        mydict = json.loads(arg1)
        
        #print (type(self.controlWidget.getCurrentWidget()))
        try:
            astroTable = self.controlWidget.getCurrentWidget().prepareTabularOutput(mydict)
            self.tableWidget.setContent(astroTable)
        except AttributeError:
            print ('MainWindow->foo->attribute not found')
            
    def setFov(self, fov):
        self.esaskyBrowserWidget.page().runJavaScript("setFov("+str(fov)+")")
        
    def initTest(self):
        print('sending initTest')
        self.esaskyBrowserWidget.page().runJavaScript("initTest()")
        
class ESASkyWrapper(QWebEngineView):

    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        
        pathlib.Path(__file__).parent.absolute()
        print (pathlib.Path(__file__).parent.absolute())
        path = str(pathlib.Path(__file__).parent.absolute())+'/index.html'
        url = QUrl.fromLocalFile(path)
        self.load(url)        
        self.show()

class ResultTable(QWidget):
    
    def __init__(self):
        super(ResultTable, self).__init__()
        self.__layout()
        
    def __layout(self):
         
        
        self.container = QWidget()
        
        self.tableWidget = QTableWidget()
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout)
        
        
        
    def setContent(self, astroTable):
        
        self.tableWidget.setRowCount(len(astroTable))
        self.tableWidget.setColumnCount(len(astroTable.colnames))
        self.tableWidget.setHorizontalHeaderLabels(astroTable.colnames)

        rowIdx = 0
        colIdx = 0
        for row in astroTable:
            for header in astroTable.colnames:
                self.tableWidget.setItem(rowIdx, colIdx, QTableWidgetItem(str(astroTable[rowIdx][header])))
                colIdx = colIdx + 1
            rowIdx = rowIdx + 1
            colIdx = 0
        
    
class ControlBox(QWidget):
    
    def __init__(self, esaskyWrapper):
        super(ControlBox, self).__init__()
        
        self.esaskyWrapper = esaskyWrapper
        self.__layout()
        self.currentWidget = None
        
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
        
        
        resultLabel = QLabel('result', self)
        self.resultText = QLabel('', self)
        self.resultText.setWordWrap(True)
        self.resultTableWidgetArea = QWidget()
        rLayout = QVBoxLayout()
        rLayout.addWidget(resultLabel)
        rLayout.addWidget(self.resultText)
        rLayout.addWidget(self.resultTableWidgetArea)
        resultWidget = QWidget()
        resultWidget.setLayout(rLayout)
     
        
        controlBoxWidget = QWidget()
        self.vControlBoxLayout = QVBoxLayout()
        self.vControlBoxLayout.addWidget(self.esaskyAPIList)
        self.vControlBoxLayout.addWidget(self.stack)
        self.vControlBoxLayout.addWidget(resultWidget)
        
        controlBoxWidget.setLayout(self.vControlBoxLayout)
        self.setLayout(self.vControlBoxLayout)

    def displayWidget(self, i):
        #self.setResultText('')
        self.stack.setCurrentIndex(i)
        self.currentWidget = self.stack.widget(i)
        try:
            self.currentWidget.directRun()
        except AttributeError:
            print ('ControlBox->displayWidget->attribute not found')
    
    def getCurrentWidget(self):
        return self.currentWidget    
    
    def setResultTable(self, tableWidget):
        #self.resultTableWidgetArea.
        pass

showCommands = True

if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    view = MainWindow()
    
    desktop = QDesktopWidget()
    width = desktop.width()*0.8;
    height = desktop.height()*0.8;
    view.setFixedSize(width,height);
    view.show()
    
    #QObject.emit(SIGNAL("testInit"))
    app.exec_()
        
