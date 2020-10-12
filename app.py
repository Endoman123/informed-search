import sys
import gridworld
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AppWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        toolbar = self.build_toolbar() 
        grid = self.build_grid()

        self.addToolBar(toolbar)

        self.centerWidget = grid 
    
            
    def build_toolbar(self):
        ret = QToolBar()
    
        a_new = QAction("New", self)
        a_save = QAction("Save", self)
        a_open = QAction("Open", self)
    
        a_new.setShortcut("Ctrl+N")
        a_save.setShortcut("Ctrl+S")
        a_open.setShortcut("Ctrl+O")
    
        ret.addAction(a_new) 
        ret.addAction(a_save)
        ret.addAction(a_open)
        
        return ret
    
    def build_grid(self):
        ret = QWidget()
        container = QVBoxLayout() 
        grid = QGridLayout()
    
        container.addLayout(grid) 
        ret.setLayout(container)

        return ret

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show() 
    sys.exit(app.exec_())
