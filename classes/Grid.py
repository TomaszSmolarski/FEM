from classes.UniversalElement import UniversalElement as ue
from classes.Element import Element
from classes.Node import Node


class Grid:

    def __init__(self, gd):
        self.ld=gd
        self.dx = gd.W / (gd.nW - 1)
        self.dy = gd.H / (gd.nH - 1)
        self.nodes = [Node(id=nr + 1) for nr in range(gd.nN)]
        self.set_nodes(gd)
        self.elements = [self.set_element(gd, nr) for nr in range(gd.nE)]

    def set_nodes(self, gd):
        xx = 0
        yy = 0
        nr = 0
        BC = False
        while gd.nN > nr:
            if xx == 0 or yy == 0 or xx == gd.W or yy == gd.H:
                BC = True
            # self.nodes.append(node(0, xx, yy,BC, nr + 1))
            self.nodes[nr] = Node( nr + 1,0, xx, yy, BC)
            BC = False
            nr = nr + 1
            if nr != 0 and nr % gd.nH == 0:
                xx = xx + self.dx
                yy = 0
            else:
                yy = yy + self.dy

    def set_element(self, gd, nr):
        j = int(nr / (gd.nH - 1))
        nodesArray = []
        trueArrayNodes = []
        wallAmount = 0
        wallNumbers = []
        nodesArray.append(self.nodes[nr + j])
        nodesArray.append(self.nodes[nr + j + gd.nH])
        nodesArray.append(self.nodes[nr + j + gd.nH + 1])
        nodesArray.append(self.nodes[nr + j + 1])

        for node in nodesArray:
            if node.bc == True:
                trueArrayNodes.append(node)
                wallAmount = wallAmount + 1
        if wallAmount > 0:
            wallAmount = wallAmount - 1

            if len(trueArrayNodes) == 2:
                if abs(trueArrayNodes[0].id - trueArrayNodes[1].id) == 1:
                    if trueArrayNodes[0].id < gd.nH:
                        wallNumbers.append(4)
                    else:
                        wallNumbers.append(2)
                elif trueArrayNodes[0].id & gd.nH == 0:
                    wallNumbers.append(3)
                else:
                    wallNumbers.append(1)

            elif len(trueArrayNodes) == 3:
                if any(node.id & gd.nH == 0 for node in trueArrayNodes):
                    if any(node.id == gd.nH for node in trueArrayNodes):
                        wallNumbers.append(3)
                        wallNumbers.append(4)
                    else:
                        wallNumbers.append(2)
                        wallNumbers.append(3)
                elif all(node.id > gd.nH for node in trueArrayNodes):
                    wallNumbers.append(1)
                    wallNumbers.append(2)
                else:
                    wallNumbers.append(1)
                    wallNumbers.append(4)

        elem = Element(nr+1,nodesArray, wallNumbers, wallAmount)

        return elem

