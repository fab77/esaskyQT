from PyQt5.QtWidgets import QHBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QComboBox

class AbstractWidget(QWidget):
    
    def __init__(self, esaskyWrapper):
        super(AbstractWidget, self).__init__()
        self.esaskyWrapper = esaskyWrapper
    
    def getESASkyWrapper(self):
        return self.esaskyWrapper;
    
    def directRun(self):
        print('AbstractWidget -> run')
        pass
    
    def onClick(self):
        pass

class FovBox(AbstractWidget):
    
    def __init__(self, esaskyWrapper):
        super(FovBox, self).__init__(esaskyWrapper)
        self.__layout()
        
    def __layout(self):
        
        # FoV box
        label = QLabel('FoV in degrees: ', self)
        self.inputText = QLineEdit(self)
        self.inputText.setPlaceholderText('20.4')
        self.inputText.setMinimumWidth(1)
        button = QPushButton("set FoV")
        button.clicked.connect(self.onClick)
        button.show()
        
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(label)
        self.hLayout.addWidget(self.inputText)
        self.hLayout.addWidget(button)
        self.setLayout(self.hLayout)
        
    def directRun(self):
        pass
        
    def onClick(self):
        print ('Clicked on changeFov')
        self.esaskyWrapper.page().runJavaScript("setFov("+self.inputText.text()+")")


class GoToTargetName(AbstractWidget):
    
    def __init__(self, esaskyWrapper):
        super(GoToTargetName, self).__init__(esaskyWrapper)
        self.__layout()
        
    def __layout(self):
        
        label = QLabel('Target name: ', self)
        self.inputText = QLineEdit(self)
        self.inputText.setPlaceholderText('M51 or coords')
        self.inputText.setMinimumWidth(1)
        button = QPushButton("search")
        button.clicked.connect(self.onClick)
        button.show()
        
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(label)
        self.hLayout.addWidget(self.inputText)
        self.hLayout.addWidget(button)
        self.setLayout(self.hLayout)
        
    def directRun(self):
        pass
        
    def onClick(self):
        print ('Clicked on ')
        self.esaskyWrapper.page().runJavaScript("goToTargetName('"+self.inputText.text()+"')")
    
class GetAvailableHiPS(AbstractWidget):
    
    def __init__(self, esaskyWrapper):
        super(GetAvailableHiPS, self).__init__(esaskyWrapper)
        self.__layout()
        
    def __layout(self):
        
        label = QLabel('Wavelength: ', self)
        
        self.combo = QComboBox()
        self.combo.addItems(["-", "All", "GAMMA_RAY", "HARD_X_RAY", "SOFT_X_RAY", "UV", "OPTICAL", "NEAR_IR", "MID_IR", "FAR_IR", "SUBMM", "RADIO", "OTHERS"])
        self.combo.currentIndexChanged.connect(self.onClick)
        
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(label)
        self.hLayout.addWidget(self.combo)
        self.setLayout(self.hLayout)
    
    
    def directRun(self):
        pass
        
    def onClick(self):
        print ('Clicked on ')
        self.esaskyWrapper.page().runJavaScript("getAvailableHiPS('"+self.combo.currentText()+"')")
    

class CataloguesCount(AbstractWidget):
    
    def __init__(self, esaskyWrapper):
        super(CataloguesCount, self).__init__(esaskyWrapper)
        
        
    def directRun(self):
        print ('CataloguesCount -> run')
        self.esaskyWrapper.page().runJavaScript("getCataloguesCount()")

        