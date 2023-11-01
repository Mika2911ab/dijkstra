from graph import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def ReadCSV(G,window):
    with open('testnodes.csv')as file:
        nodedict= {}
        for line in file:
            node,lg,bg = line.split(',')
            nodedict[node] = len(nodedict)#gibt keine 2 nodes mit gleichen namen
            G.add_node(float(lg),float(bg))
            ###Knoten anzeigen
            #btn = QPushButton(window)
            #btn.setGeometry(*umrechnen(float(lg),float(bg)),10,10)  # Position und Größe des Buttons
            #btn.setStyleSheet("background-color: red; border-radius: 5px;")  # Stilvorlage für den Kreis
    #painter = QPainter(window)
    #painter.setPen(QPen(QColor('black'),4.0, Qt.PenStyle.SolidLine))
    with open('testedges.csv') as file:
        for line in file:
            n1,n2 = line.replace('\n','').split(',')
            x1,y1,x2,y2 = G.add_edge(nodedict[n1],nodedict[n2])
            #achtung jede edge a,b is auch b,a in der datei (anscheinend)
            #nichtmal geschafft linie zu machen ):
            #painter.drawLine(*umrechnen(x1, y1), *umrechnen(x2, y2))

def umrechnen(lg,bg):
    #[8.1611,8.3781]min/max längengrad
    #[49.9468,50.1082]min/max breitengrad
    #400 war länge und breite des fensters
    #ohne erde
    return (int(((lg-8.1611)/0.217)*400),int(((bg-49.9468)/0.1614)*400))
def main():
    G = Graph()
    P = PQueue()
    print(P.items,P.pos,P.first)
    P.push(1,2)
    print(P.items,P.pos,P.first)
    P.push(2,5)
    print(P.items,P.pos,P.first)
    P.push(3,3)
    print(P.items,P.pos,P.first)
    P.decrease_Key(2,1)
    print(P.items,P.pos,P.first)
    print(P.pop_min())
    print(P.items,P.pos,P.first)
    app = QApplication(sys.argv)
    window = QWidget()
    #window.setWindowTitle("Maps fake lol")
    #window.setGeometry(100,100,400,400)
    #painter = QPainter(window)
    #painter.setPen(QColor.black())
    #painter.drawLine(97,241,195,151)
    #ReadCSV(G,window)
    #window.show()
    #sys.exit(app.exec_())

main()