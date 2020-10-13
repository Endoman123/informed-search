import sys
import gridworld
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

rows = 120
cols = 160

class AppWindow(QMainWindow):
    __grid = None 
    def __init__(self, parent = None):
        super().__init__(parent)
        
        toolbar = self.buildToolbar()
        self.__grid = QGridScene() 

        toolbar.actionTriggered[QAction].connect(self.tbOnPressed)
        self.addToolBar(toolbar) 
        self.setCentralWidget(QGridView(self.__grid))         
   
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
    
    def tbOnPressed(self, event):
        if event.text == "Save":
            pass
        elif event.text == "Open":
            pass
        else:
            gridworld.initGridworld(rows, cols)
            if self.__grid:
                self.__grid.paintGridworld()
            pass

class QGridScene(QGraphicsScene):
    __WIDTH = 7 
    __HEIGHT = 7
    __cells = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grid = QGraphicsItemGroup()

        width = cols * self.__WIDTH
        height = rows * self.__HEIGHT
        
        grid.setZValue(100)
        self.addItem(grid) 
        self.setSceneRect(0, 0, width, height)
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        for x in range(0, cols + 1):
            xc = x * self.__WIDTH
            grid.addToGroup(QGraphicsLineItem(xc, 0, xc, height))

        for y in range(0, rows + 1):
            yc = y * self.__HEIGHT
            grid.addToGroup(QGraphicsLineItem(0, yc, width, yc))

    def paintGridworld(self):
        for c in self.__cells:
            self.removeItem(c) 

        if gridworld.terrain: 
            for y in range(rows):
                for x in range(cols):
                    b = QBrush(Qt.gray)
                    v = gridworld.terrain[y + 1][x + 1]
                    
                    if v.isUnblocked():
                        b.setStyle(Qt.NoBrush) 
                    elif v.isUnblocked():
                        b.setStyle(Qt.Dense6Pattern)
                    elif v.isBlocked():
                        b.setStyle(Qt.SolidPattern)
                    
                    self.__cells.append(self.addRect(x * self.__WIDTH, y * self.__HEIGHT, self.__WIDTH, self.__HEIGHT, QPen(Qt.NoPen), b))


class QGridView(QGraphicsView):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.view_menu = QMenu(self)

# class GridCell(QFrame):
#     __vertex = None 
#     
#     def __init__(self, parent = None, v = None):
#         super().__init__(parent) 
#         self.setFrameStyle(QFrame.Panel) 
#         self.setAutoFillBackground(True) 
#         self.__vertex = v
# 
#     def setVertex(self, v):
#         self.__vertex = v
# 
#     def paintEvent(self, event):
#         v = self.__vertex
#         palette = self.palette()
#         painter = QPainter()   
# 
#         painter.begin(self)
# 
#         if v != None:
#             if v.isUnblocked():
#                 palette.setColor(self.backgroundRole(), Qt.yellow)
#         else:
#             palette.setColor(self.backgroundRole(), Qt.black)
# 
#         painter.end()
# 
#         self.setPalette(palette)
#         super().paintEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show() 
    sys.exit(app.exec_())
