import math

###nodes sind tupel (längengrad,breitengrad,Adjazensliste von ausgehenden Kanten)
###edges sind tupel (from_node,to_node,abstand denk ich mal macht sinn)
class PQueue:
    def __init__(self):
        self.items = []
        self.first = 0
        self.pos = {}
    def push(self,u,value):
        self.items.append((u,value))
        self.pos[u] = len(self.items)-1
        self.decrease_Key(u,value)
    def decrease_Key(self,u,value):
        j = self.pos[u]
        while j > self.first and self.items[j - 1][1] > value:
            self.pos[self.items[j - 1][0]] = j
            self.items[j] = self.items[j - 1]
            j -= 1
        self.items[j] = (u, value)
        self.pos[u] = j
        #
    def pop_min(self):
        self.first += 1
        return self.items[self.first-1]

def Abstand(l1,b1,l2,b2):
    b = 111.3*math.cos((b1+b2)*math.pi/360)
    return math.sqrt((b*(l1-l2))**2+(111.3 *(b1-b2))**2)
    #return math.sqrt((l1-l2)**2+(b1-b2)**2)

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.nodevalues = []#kann auch in den tupel wie bei edge für dijkstra anpassen
    def add_node(self,l,b):#nodes müssen in der reihnfolge geadded werden wie sie heißen
        self.nodes.append((l,b,[]))
        self.nodevalues.append(None)
    def add_edge(self,n1,n2):
        (l1,b1, al1) = self.nodes[n1]
        (l2, b2, al2) = self.nodes[n2]
        dist = Abstand(l1,b1,l2,b2)
        self.edges.append((n1,n2,dist))
        self.nodes[n1] = (l1,b1,al1+[(n1,n2,dist)])#hier vllt den index statt edge selbst
        return (l1,b1,l2,b2)
    def num_nodes(self):
        return len(self.nodes)
    def num_edges(self):
        return len(self.edges)
    def from_node(self,e):
        r,_ = e
        return r
    def to_node(self,e):
        _, r = e
        return r
    def out_edges(self,u):
        _,_,a = self.nodes[u]
        return a
    def in_edges(self,u):
        a = self.out_edges(u)
        return [(n2,n1,dist) for (n1,n2,dist) in a]#weil sowieso immer beide existieren
    def set_node_value(self,u,value):
        self.nodevalues[u] = value
    def node_value(self,u):
        return self.nodevalues[u]

