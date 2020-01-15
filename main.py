from classes.Element import Element
from classes.GlobalData import GlobalData
from classes.Node import Node
from classes import Grid
from classes.Calculations import *
from classes import UniversalElement
import numpy as np
import json


def main():

    with open("data_file.json", "r") as read_file:
        data = json.load(read_file)
    '''
    gd = GlobalData(1.5, 0.5, 6, 4)
    nodesArray = []
    nodesArray.append(Node(id=1, x=0, y=0, bc=True))
    nodesArray.append(Node(id=2, x=0.025, y=0, bc=True))
    nodesArray.append(Node(id=3, x=0.025, y=0.025, bc=True))
    nodesArray.append(Node(id=4, x=0, y=0.025, bc=False))
    ele = Element(1, nodesArray)
    #print(jakobian_matrix(ele))
    #print(c_matrix(ele, 7800, 700))
    print(h_matrix(ele,30,25))
    #print(jakobian_matrix(ele))
    #print(ele)
    #print(p_matrix(ele,25,1))


    #print(length_of_sizes(ele))
    #print(jakobian_matrix(ele))
    #print(np.linalg.inv(jakobian_matrix(ele)))
    #print(local_to_global(ele))
    #print(h_bc_matrix_1d(ele, 25))
    print(p_matrix(ele,25,1))
    #print(jakobian_matrix(ele))
    '''

    gd2 = GlobalData(data['H'], data['W'], data['nH'], data['nW'])
    siatka = Grid(gd2)

    print("##########################################")
    print(h_global(siatka, data['conductivity'], data['alpha']))
    print("##########################################")
    print(c_global(siatka, data['density'], data['specific_heat']))
    print("##########################################")
    print(p_global(siatka, data['alpha'], data['ambient_temp']))
    simulate_heat_transfer(siatka, data['initial_temp'], data['simulation_time'], data['simulation_step_time'],
                           data['ambient_temp'], data['alpha'], data['specific_heat'], data['conductivity'],
                           data['density'])
    print("##########################################")

    gd3=GlobalData(0.1, 0.1, 31, 31)
    siatka2=Grid(gd3)
    simulate_heat_transfer(siatka2,100,100,1,1200,300,700,25,7800)



if __name__ == '__main__':
        main()
