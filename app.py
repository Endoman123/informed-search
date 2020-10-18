import sys
import os
import math
import gridworld
import ai
import a_star
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

rows = 120
cols = 160

class AppWindow(QMainWindow):
    __grid = None 
    __gridView = None
    __dialog = None
    __menu = None

    def __init__(self, parent = None):
        super().__init__(parent)
        
        toolbar = self.buildGridToolbar()
        ai = self.buildAIToolbar()
        menu = self.buildMenubar()
        grid = QGridScene() 
        gridView = QGridView(grid)

        self.setMenuBar(menu) 
        self.addToolBar(toolbar) 
        self.addToolBar(ai)
        self.setCentralWidget(gridView)         
        self.setWindowTitle("Gridworld (Informed Search)") 

        dialog = QFileDialog(self) 
        dialog.setViewMode(QFileDialog.List)
        dialog.setNameFilter("Gridworld (*.gw)")
        dialog.setDefaultSuffix("gw")

        self.__grid = grid
        self.__gridView = gridView
        self.__dialog = dialog
        self.__menu = menu

    def buildAIToolbar(self):
        ret = QToolBar("AI", self)

        ret.addAction("Uniform-Cost")
        ret.addAction("Weighted A*") 
        ret.addAction("Sequential A*")
        ret.addAction("A*") 

        ret.actionTriggered[QAction].connect(self.runAI)

        return ret

    def buildGridToolbar(self):
        ret = QToolBar("Grid View", self)
    
        a_zoomin = QAction(QIcon.fromTheme("zoom-in", QIcon("zoom-in.svg")), "Zoom +", self)
        a_zoomout = QAction(QIcon.fromTheme("zoom-out", QIcon("zoom-out.svg")), "Zoom -", self)
        a_resetzoom = QAction(QIcon.fromTheme("zoom-original", QIcon("zoom-original.svg")), "Reset Zoom", self)  

        a_zoomin.setShortcut("Ctrl+=")
        a_zoomout.setShortcut("Ctrl+-")
        a_resetzoom.setShortcut("Ctrl+0")

        ret.addAction(a_zoomin) 
        ret.addAction(a_zoomout)
        ret.addAction(a_resetzoom)
        
        ret.actionTriggered[QAction].connect(self.zoom)

        return ret

    def buildMenubar(self):
        ret = QMenuBar()
    
        mFile = ret.addMenu("File")
        a_new = mFile.addAction("New")
        a_open = mFile.addAction("Open")
        a_save = mFile.addAction("Save")
        mFile.addSeparator()
        a_quit = mFile.addAction("Quit")
       
        a_new.setShortcut("Ctrl+N")
        a_open.setShortcut("Ctrl+O")
        a_save.setShortcut("Ctrl+S")
        a_quit.setShortcut("Ctrl+Q")

        ret.triggered[QAction].connect(self.doFileAction)

        return ret

    def runAI(self, event):
        map = gridworld.terrain
        start = gridworld.start
        goal = gridworld.goal

        grid = self.__grid

        t = event.text()
       
        path = None
        
        if t == "Uniform-Cost":
            info = a_star.uniform(map, start, goal)
        elif t == "Weighted A*":
            info = a_star.weighted(map, start, goal)
        elif t == "Sequential A*": 
            info = a_star.sequential(map, start, goal) 
        elif t == "A*":
            info = a_star.a_regular(map, start, goal)
        else:
            pass

        if info:
            grid.displayPathfinding(info)    

    def zoom(self, event):
        view = self.__gridView
        t = event.text()
        if t == "Zoom +":
            view.zoom(10)
        elif t == "Zoom -":
            view.zoom(0.1)
        else:
            view.resetZoom()

    def doFileAction(self, event): 
        t = event.text() 
        dialog = self.__dialog
        grid = self.__grid
        if t == "New":
            gridworld.initGridworld()
            grid.updateScene()
        elif t == "Save":
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setAcceptMode(QFileDialog.AcceptSave)
            if dialog.exec():
                gridworld.writeGridworld(dialog.selectedFiles()[0])
        elif t == "Open":
            dialog.setFileMode(QFileDialog.ExistingFile)
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            if dialog.exec():
                gridworld.loadGridworld(dialog.selectedFiles()[0])
                grid.updateScene()
        else:
            QApplication.quit()

class QGridScene(QGraphicsScene):
    __WIDTH = 7 
    __HEIGHT = 7
    __cells = None
    __highways = None 
    __start = None
    __goal = None
    __path = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cells = QGraphicsItemGroup()
        highways = QGraphicsItemGroup() 
        points = QGraphicsItemGroup()
        grid = QGraphicsItemGroup()
        path = QGraphicsItemGroup()

        width = cols * self.__WIDTH
        height = rows * self.__HEIGHT
       
        cells.setZValue(0) 
        grid.setZValue(1)
        highways.setZValue(2)
        points.setZValue(3)
        path.setZValue(4)

        self.addItem(cells) 
        self.addItem(grid)
        self.addItem(highways) 
        self.addItem(points)
        self.addItem(path)

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
        self.__path = path

    def updateScene(self):
        self.__start.setPos((gridworld.start[0] - 1) * self.__WIDTH, (gridworld.start[1] - 1) * self.__HEIGHT)
        self.__goal.setPos((gridworld.goal[0] - 1) * self.__WIDTH, (gridworld.goal[1] - 1) * self.__HEIGHT)

        self.__start.setVisible(True)
        self.__goal.setVisible(True)
        
        for c in self.__path.childItems():
            self.removeItem(c)

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
                    cells[y * cols + x].setToolTip(f"({x}, {y})")

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
 
    def displayPathfinding(self, info):
        path = self.__path  
        cells = self.__cells.childItems() 
        parent = None

        map = info['map']
        f = info['f']
        g = info['g']
        h = info['h']

        for c in path.childItems():
            self.removeItem(c)

        for v in map:
            xc = (v[0] - 1) * self.__WIDTH + 0.5 * self.__WIDTH
            yc = (v[1] - 1) * self.__HEIGHT + 0.5 * self.__HEIGHT 

            if parent != None:
                pxc = (parent[0] - 1) * self.__WIDTH + 0.5 * self.__WIDTH
                pyc = (parent[1] - 1) * self.__HEIGHT + 0.5 * self.__HEIGHT 
                line = QGraphicsLineItem(xc, yc, pxc, pyc)
                line.setPen(QPen(Qt.red))
                path.addToGroup(line)

            parent = v

        for y in range(rows):
            for x in range(cols):
                v_f = f[y + 1][x + 1]
                v_g = g[y + 1][x + 1]
                v_h = h[y + 1][x + 1]

                tt = f"({x}, {y})" + os.linesep
                tt += f"f: {v_f}" + os.linesep
                tt += f"g: {v_g}" + os.linesep
                tt += f"h: {v_h}" + os.linesep

                cells[y * cols + x].setToolTip(tt)

class QGridView(QGraphicsView):
    __zoom = 1
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.view_menu = QMenu(self)

    def zoom(self, v):
        self.__zoom *= v
        self.scale(v, v)

    def resetZoom(self):
        v = 1 / self.__zoom
        self.scale(v, v)
        self.__zoom = 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show() 
    sys.exit(app.exec_())
