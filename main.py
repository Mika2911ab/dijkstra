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
def Dijksrtra(G,s,t):
    # 0 weiß ,1 grau,2 schwarz
    S = []
    for i in range(G.num_nodes()):
        G.set_node_value(i, (0,math.inf,[]))
    P = PQueue()
    P.push(s,0)
    while True:
        (n,dist) = P.pop_min()
        _,_,path = G.node_value(n)
        G.set_node_value(n, (2, dist,path))
        if n == t:
            return path
        for (a,b,edge_dist) in G.out_edges(n):
            (c,node_dist,_) = G.node_value(b)
            if  c == 2:
                continue
            elif(c == 0):
                P.push(b,dist+edge_dist)
                G.set_node_value(b,(1,dist+edge_dist,path+[(a,b)]))
            elif(dist+edge_dist < node_dist):
                P.decrease_Key(b,dist+edge_dist)
                G.set_node_value(b, (1, dist + edge_dist, path+(a, b)))



def main():
    G = Graph()
    app = QApplication(sys.argv)
    window = QWidget()
    #window.setWindowTitle("Maps fake lol")
    #window.setGeometry(100,100,400,400)
    #painter = QPainter(window)
    #painter.setPen(QColor.black())
    #painter.drawLine(97,241,195,151)
    ReadCSV(G,window)
    print(Dijksrtra(G,0,2))
    #window.show()
    #sys.exit(app.exec_())

main()