from classes.Element import Element
from classes.GlobalData import GlobalData
from classes.Node import Node
from classes import Grid
from classes.Calculations import *
from classes import  UniversalElement
import numpy as np
def main():
    gd = GlobalData(1.5, 0.5, 6, 4)
    ue=UniversalElement.UniversalElement()
    nodesArray = []

    nodesArray.append(Node(id=1, x=0, y=0, bc=True))
    nodesArray.append(Node(id=2, x=0.025, y=0, bc=True))
    nodesArray.append(Node(id=3, x=0.025, y=0.025, bc=True))
    nodesArray.append(Node(id=4, x=0, y=0.025, bc=False))
    ele = Element(1,nodesArray,[1],1)
    '''
    print(c_matrix(ele, ue, 7800, 700))
    print(h_matrix(ele,ue,30,25))
    print(length_of_sizes(ele, ue))
    print(jakobian_matrix(ele, ue))
    print(np.linalg.inv(jakobian_matrix(ele, ue)))
    print(dNdxdNdyM(ele,ue))
    print(local_to_global(ele,ue))
    print(h_bc_matrix_2d(ele, ue, 25))
    print(h_bc_matrix_1d(ele, ue, 25))
    print(p_matrix(ele,ue,25,1))
    '''

    gd2=GlobalData(0.1,0.1,4,4)
    siatka = Grid(gd2)
    print(siatka.nodes)
    print(siatka.elements)
    '''
    print(siatka.nodes[3])
    print(siatka.elements)
    print(siatka.elements[9])
    print(siatka.elements[9].nodes)
    print(siatka.elements[9].nodes[1])
    '''

if __name__ == '__main__':
    main()
