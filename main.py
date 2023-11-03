from graph import *
import sys
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def ReadCSV(G):
    with open('nodes.csv') as file:
        nodedict = {}
        for line in file:
            node, lg, bg = line.split(',')
            nodedict[node] = len(nodedict)  # gibt keine 2 nodes mit gleichen namen
            G.add_node(float(lg), float(bg))
            ###Knoten anzeigen
            # btn = QPushButton(window)
            # btn.setGeometry(*umrechnen(float(lg),float(bg)),10,10)  # Position und Größe des Buttons
            # btn.setStyleSheet("background-color: red; border-radius: 5px;")  # Stilvorlage für den Kreis
    # painter = QPainter(window)
    # painter.setPen(QPen(QColor('black'),4.0, Qt.PenStyle.SolidLine))
    with open('edges.csv') as file:
        for line in file:
            n1, n2 = line.replace('\n', '').split(',')
            x1, y1, x2, y2 = G.add_edge(nodedict[n1], nodedict[n2])
            # achtung jede edge a,b is auch b,a in der datei (anscheinend)
            # nichtmal geschafft linie zu machen ):
            # painter.drawLine(*umrechnen(x1, y1), *umrechnen(x2, y2))

def Dijksrtra(G, s, t):
    # 0 weiß ,1 grau,2 schwarz
    S = []
    for i in range(G.num_nodes()):
        G.set_node_value(i, (0, math.inf, []))
    P = PQueue()
    P.push(s, 0)
    while True:
        (n, dist) = P.pop_min()
        _, _, path = G.node_value(n)
        G.set_node_value(n, (2, dist, path))
        if n == t:
            return path
        for (a, b, edge_dist) in G.out_edges(n):
            (c, node_dist, _) = G.node_value(b)
            if c == 2:
                continue
            elif (c == 0):
                P.push(b, dist + edge_dist)
                G.set_node_value(b, (1, dist + edge_dist, path + [(a, b)]))
            elif (dist + edge_dist < node_dist):
                P.decrease_Key(b, dist + edge_dist)
                G.set_node_value(b, (1, dist + edge_dist, path + (a, b)))



class Window(QWidget, object):
    def __init__(self):
        super().__init__()

        # Größe der Fläche und point size
        self.width = 1000
        self.height = 600
        self.p_size = 0

        # timer
        self.timer = QTimer()

        # window settings
        self.setGeometry(450, 250, 1000, 600)
        self.setWindowTitle("Map")

        self.form = QFormLayout()  # Layout

        # create board
        self.board = QtGui.QPixmap(1000, 600)

        self.display = QLabel()
        self.display.setGeometry(QRect(0, 0, 1000, 400))
        self.display.setAutoFillBackground(True)
        palette = self.display.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  # Set the background color to white
        self.display.setPalette(palette)

        # Widget und Layout hinzufügen
        self.form.addWidget(self.display)
        self.setLayout(self.form)

        # hier kommt der Graph shit
        self.G = Graph()
        ReadCSV(self.G)

        # outer stuff
        self.calcOuterVal()

        # world
        self.world = self.standardMap()
        self.world_img = QImage(self.world.data, 1000, 600, QImage.Format_RGBA8888)

        self.mappainter = QPainter(self.world_img)
        self.mappainter.setPen(QColor(0, 0, 0))
        self.mappainter.setBrush(QColor(0, 0, 0))

        self.drawCons()

        self.timerFun()

    def timerFun(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.onRepeat)
        self.timer.start()

    def calcOuterVal(self):
        self.minlong = self.G.nodes[0][1]
        self.maxlong = self.G.nodes[0][1]

        self.maxlat = self.G.nodes[0][0]
        self.minlat = self.G.nodes[0][0]
        for i in self.G.nodes:
            if i[1] < self.minlong:
                self.minlong = i[1]
            elif i[1] > self.maxlong:
                self.maxlong = i[1]
            if i[0] < self.minlat:
                self.minlat = i[0]
            elif i[0] > self.maxlat:
                self.maxlat = i[0]

    def umrechnen(self, lg, bg):

        # [8.1611,8.3781]min/max längengrad     self.minlat/ self.maxlat
        # [49.9468,50.1082]min/max breitengrad  self.minlong/ self.maxlong
        # 400 war länge und breite des fensters
        # ohne erde
        return (int(((lg - self.minlat) / 0.217) * self.width), int(((bg - self.minlong) / 0.1614) * self.height))          # ToDo: teilungsfaktoren variable machen

    def drawCons(self):
        for edge in self.G.edges:
            node_out = self.G.nodes[edge[0]]
            node_in = self.G.nodes[edge[1]]

            x1, y1 = self.umrechnen(node_out[0], node_out[1])
            x2, y2 = self.umrechnen(node_in[0], node_in[1])

            self.mappainter.drawLine(x1, self.height - y1, x2, self.height - y2)
    def standardMap(self):
        # Erstellen eines leeren 2D Numpy-Arrays mit den Dimensionen width x height und 3 Kanälen (RGB)
        world = np.zeros((self.height, self.width, 4), dtype=np.uint8)

        for x in range(self.width):
            for y in range(self.height):
                world[y, x] = [255, 255, 255, 255]

        for i in self.G.nodes:
            tempx, tempy = self.umrechnen(float(i[0]), float(i[1]))
            if (self.height-tempy < self.height and tempx < self.width):
                world[self.height-tempy, tempx] = [0, 0, 0, 255]

            for x in range(-self.p_size, self.p_size):
                for y in range(-self.p_size, self.p_size):
                    tempx2 = tempx + x
                    tempy2 = tempy + y
                    if(self.height-tempy2<self.height and tempx2 < self.width):
                        world[self.height - tempy2, tempx2] = [0, 0, 0, 255]

        return world
    def onRepeat(self):
        # temporäres Bild (Kopie von world_img)
        self.temp_img = QImage(self.world_img)

        # Painter für temp
        temppainter = QPainter(self.temp_img)
        #
        self.display.setPixmap((QPixmap.fromImage(self.temp_img)))


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()

    app.exec()


main()
