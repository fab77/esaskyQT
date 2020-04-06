from PyQt5.QtWidgets import QHBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QComboBox
from astropy.table import Table

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
    
    def prepareTabularOutput(self, content):
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

    def prepareTabularOutput(self, content):
        pass

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
    
    def prepareTabularOutput(self, content):
        pass
    
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
    
    def prepareTabularOutput(self, content):
        print('GetAvailableHiPS->prepareTabularOutput')
        '''
        {'values': {
            'INTEGRAL-IBIS RGB': {
                'HiPS label': 'INTEGRAL-IBIS RGB', 
                'HiPS URL': '//cdn.skies.esac.esa.int/Integral/color/', 
                'hips_frame': 'equatorial', 
                'maxOrder': '3', 
                'format': 'jpg'
                }, 
            'INTEGRAL-IBIS 20-35 keV': {
                'HiPS label': 'INTEGRAL-IBIS 20-35 keV', 
                'HiPS URL': '//cdn.skies.esac.esa.int/Integral/20-35/', 
                'hips_frame': 'equatorial', 
                'maxOrder': '3', 
                'format': 'jpg'
                }, 
            'INTEGRAL-IBIS 35-65 keV': {
                'HiPS label': 'INTEGRAL-IBIS 35-65 keV', 
                'HiPS URL': '//cdn.skies.esac.esa.int/Integral/35-65/', 
                'hips_frame': 'equatorial', 
                'maxOrder': '3', 
                'format': 'jpg'
                }, 
            'INTEGRAL-IBIS 65-100 keV': {
                'HiPS label': 'INTEGRAL-IBIS 65-100 keV', 
                'HiPS URL': '//cdn.skies.esac.esa.int/Integral/65-100/', 
                'hips_frame': 'equatorial', 
                'maxOrder': '3', 
                'format': 'jpg'
                }, 
            'Swift-BAT RGB': {
                'HiPS label': 'Swift-BAT RGB', 
                'HiPS URL': '//cdn.skies.esac.esa.int/swift_bat_flux/', 
                'hips_frame': 'equatorial', 
                'maxOrder': '6', 
                'format': 'png'
                }
            }, 
        'msgId': 11
        }
        '''
        t = Table(names=('HiPS name', 'root URL', 'coordinate frame', 'max norder', 'format'), dtype=('S15', 'S40', 'S12', 'i2', 'S4'))
        for key, item in content.items():
            if key == 'values':
                
                for attribute, value in item.items():
                    currRow = []
                    for hipsColumnDetails, hipsValue in value.items():
                        currRow.append(hipsValue)
                    t.add_row(currRow)
        return t
        

class CataloguesCount(AbstractWidget):
    
    def __init__(self, esaskyWrapper):
        super(CataloguesCount, self).__init__(esaskyWrapper)
        
        
    def directRun(self):
        print ('CataloguesCount -> run')
        self.esaskyWrapper.page().runJavaScript("getCataloguesCount()")

    def prepareTabularOutput(self, content):
        print('CataloguesCount->prepareTabularOutput')
        print(content)
        t = Table(names=('dataset', 'count'), dtype=('S20', 'i4'))
        
        for key, item in content.items():
            if key == 'values':
                
                for attribute, value in item.items():
                    currRow = []
                    currRow.append(attribute)
                    currRow.append(value)
                    t.add_row(currRow)
        return t
    