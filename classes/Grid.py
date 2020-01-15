from classes.UniversalElement import UniversalElement as ue
from classes.Element import Element
from classes.Node import Node
from classes.GlobalData import GlobalData


class Grid:

    def __init__(self, gd: GlobalData):
        self.__ld = gd
        self.__dx = self.ld.W / (self.ld.nW - 1)
        self.__dy = self.ld.H / (self.ld.nH - 1)
        self.__nodes = [Node(id=nr + 1) for nr in range(self.ld.nN)]
        self.__set_nodes(self.ld)
        self.__elements = [self.__set_element(self.ld, nr) for nr in range(self.ld.nE)]

    @property
    def nodes(self):
        return self.__nodes

    @property
    def elements(self):
        return self.__elements

    @property
    def dx(self):
        return self.__dx

    @property
    def dy(self):
        return self.__dy

    @property
    def ld(self):
        return self.__ld

    def __set_nodes(self, gd):
        xx = 0
        yy = 0
        nr = 0
        BC = False
        while gd.nN > nr:
            if xx == 0 or yy == 0 or xx == gd.W or yy == gd.H:
                BC = True
            self.nodes[nr] = Node(nr + 1, 0, xx, yy, BC)
            BC = False
            nr = nr + 1
            if nr != 0 and nr % gd.nH == 0:
                xx = xx + self.dx
                yy = 0
            else:
                yy = yy + self.dy

    def __set_element(self, gd: GlobalData, nr: int):
        j = int(nr / (gd.nH - 1))
        nodes_array = [self.nodes[nr + j], self.nodes[nr + j + gd.nH], self.nodes[nr + j + gd.nH + 1],
                       self.nodes[nr + j + 1]]
        elem = Element(nr + 1, nodes_array)
        return elem
