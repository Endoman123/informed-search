import sys
import gridworld
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

rows = 120
cols = 160

class AppWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        toolbar = self.buildToolbar()
        grid = self.buildGrid() 

        toolbar.actionTriggered[QAction].connect(self.tbOnPressed)
        self.addToolBar(toolbar) 
        self.setCentralWidget(grid)         
   
    def buildToolbar(self):
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
    
    def buildGrid(self):
        ret = QWidget()
        container = QVBoxLayout() 
        grid = QGridLayout()
       
        grid.setSpacing(0)
 
        for i in range(rows):
            for j in range(cols):
                grid.addWidget(GridCell(self), i, j) 
        
        container.addLayout(grid) 
        ret.setLayout(container)

        return ret

    def tbOnPressed(self, event):
        if event.text == "Save":
            pass
        elif event.text == "Open":
            pass
        else:
            gridworld.initGridWorld(rows, cols)

class GridCell(QFrame):
    __vertex = None 
    
    def __init__(self, parent = None, v = None):
        super().__init__(parent) 
        self.setFrameStyle(QFrame.Panel) 
        self.__vertex = v

    def paintEvent(self, event):
        v = self.__vertex
        palette = self.palette()
        painter = QPainter()   

        painter.begin(self)

        if v != None:
            if v.isUnblocked():
                palette.setColor(self.backgroundRole(), Qt.yellow)
        else:
            palette.setColor(self.backgroundRole(), Qt.black)

        painter.end()

        self.setPalette(palette)
        super().paintEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show() 
    sys.exit(app.exec_())
