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
    __cells = None
    __highways = None 
    __start = None
    __goal = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cells = QGraphicsItemGroup()
        highways = QGraphicsItemGroup() 
        points = QGraphicsItemGroup()
        grid = QGraphicsItemGroup()
         
        width = cols * self.__WIDTH
        height = rows * self.__HEIGHT
        
        cells.setZValue(0) 
        grid.setZValue(1)
        highways.setZValue(2)
        points.setZValue(3)
         
        self.addItem(cells) 
        self.addItem(grid)
        self.addItem(highways) 
        self.addItem(points)

        self.setSceneRect(0, 0, width, height)
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        self.__start = QGraphicsRectItem(0, 0, self.__WIDTH, self.__HEIGHT)
        self.__goal = QGraphicsRectItem(0, 0, self.__WIDTH, self.__HEIGHT)  

        p_start = QPen(Qt.green)
        p_end = QPen(Qt.red)
        p_start.setWidth(2)
        p_end.setWidth(2)
        self.__start.setPen(p_start)
        self.__start.setBrush(QBrush(Qt.NoBrush))
        self.__goal.setPen(p_end)
        self.__goal.setBrush(QBrush(Qt.NoBrush))

        self.__start.setVisible(False)
        self.__goal.setVisible(False)

        points.addToGroup(self.__start)
        points.addToGroup(self.__goal)

        for i in range(rows):
            for j in range(cols):
                cells.addToGroup(QGraphicsRectItem(j * self.__WIDTH, i * self.__HEIGHT, self.__WIDTH, self.__HEIGHT))

        for x in range(0, cols + 1):
            xc = x * self.__WIDTH
            grid.addToGroup(QGraphicsLineItem(xc, 0, xc, height))

        for y in range(0, rows + 1):
            yc = y * self.__HEIGHT
            grid.addToGroup(QGraphicsLineItem(0, yc, width, yc))

        self.__cells = cells
        self.__highways = highways

    def paintGridworld(self):
        self.__start.setPos((gridworld.start[0] - 1) * self.__WIDTH, (gridworld.start[1] - 1) * self.__HEIGHT)
        self.__goal.setPos((gridworld.goal[0] - 1) * self.__WIDTH, (gridworld.goal[1] - 1) * self.__HEIGHT)

        self.__start.setVisible(True)
        self.__goal.setVisible(True)

        for c in self.__highways.childItems():
            self.removeItem(c)

        if gridworld.terrain: 
            cells = self.__cells.childItems() 
            for y in range(rows):
                for x in range(cols):
                    v = gridworld.terrain[y + 1][x + 1] 
                    b = QBrush(Qt.NoBrush)

                    if v.isHardToTraverse():
                        b.setColor(Qt.darkGreen)
                        b.setStyle(Qt.DiagCrossPattern)
                    elif v.isBlocked():
                        b.setColor(Qt.gray)
                        b.setStyle(Qt.SolidPattern)
            
                    cells[y * cols + x].setBrush(b)
                    cells[y * cols + x].setToolTip(repr(v))

                    if v.isHighway():
                        v_n = gridworld.terrain[y][x + 1]
                        v_s = gridworld.terrain[y + 2][x + 1]
                        v_w = gridworld.terrain[y + 1][x]
                        v_e = gridworld.terrain[y + 1][x + 2]

                        p_hw = QPen(Qt.blue)
                        p_hw.setWidth(2)

                        xc = x * self.__WIDTH + 0.5 * self.__WIDTH
                        yc = y * self.__HEIGHT + 0.5 * self.__HEIGHT
                        
                        if v_n.isHighway():
                            h = QGraphicsLineItem(xc, yc, xc, yc - 0.5 * self.__HEIGHT)
                            h.setPen(p_hw)
                            self.__highways.addToGroup(h)

                        if v_s.isHighway():
                            h = QGraphicsLineItem(xc, yc, xc, yc + 0.5 * self.__HEIGHT)
                            h.setPen(p_hw)
                            self.__highways.addToGroup(h)

                        if v_w.isHighway():
                            h = QGraphicsLineItem(xc, yc, xc - 0.5 * self.__WIDTH, yc)
                            h.setPen(p_hw)
                            self.__highways.addToGroup(h)

                        if v_e.isHighway():
                            h = QGraphicsLineItem(xc, yc, xc + 0.5 * self.__WIDTH, yc)
                            h.setPen(p_hw)
                            self.__highways.addToGroup(h)
 
    def displayPathfinding(self):
        for i in range(rows):
            for j in range(cols):
                pass

class QGridView(QGraphicsView):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.view_menu = QMenu(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show() 
    sys.exit(app.exec_())
