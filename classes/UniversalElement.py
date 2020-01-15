from math import sqrt
import numpy as np


class UniversalElement:
    def __init__(self):
        self.NPc = 2  # powinny byćjeszcze wagi ale są 1 i 1 dla tego przypadku
        self.PcM = np.array([1 / sqrt(3),-(1 / sqrt(3))])
        self.weights = [1,1]
        self.Pc = np.array([[self.PcM[1], self.PcM[1]], [self.PcM[0], self.PcM[1]], [self.PcM[0], self.PcM[0]], [self.PcM[1], self.PcM[0]]])

        self.Pc_walls =np.array([[[self.Pc[0][0], -1], [self.Pc[1][0], -1]],
                   [[1, self.Pc[1][1]], [1, self.Pc[2][1]]],
                   [[self.Pc[2][0], 1], [self.Pc[3][0], 1]],
                   [[-1, self.Pc[3][1]], [-1, self.Pc[0][1]]]])
        self.M_N = self.MN()
        self.M_Ne = self.MdNde()
        self.M_Nn = self.MdNdn()

    def d1N1(self,e):
        return (1 - e)/2

    def d1N2(self,e):
        return (1 + e)/2

    def N1(self, e, n):
        return ((1 - e) * (1 - n)) / 4

    def N2(self, e, n):
        return ((1 + e) * (1 - n)) / 4

    def N3(self, e, n):
        return ((1 + e) * (1 + n)) / 4

    def N4(self, e, n):
        return ((1 - e) * (1 + n)) / 4

    def dN1e(self, e, n):
        return -(( 1-n) / 4)

    def dN1n(self, e, n):
        return -((1-e) / 4)

    def dN2e(self, e, n):
        return (1 - n) / 4

    def dN2n(self, e, n):
        return -((1 + e) / 4)

    def dN3e(self, e, n):
        return (n + 1) / 4

    def dN3n(self, e, n):
        return (e + 1) / 4

    def dN4e(self, e, n):
        return -((n + 1) / 4)

    def dN4n(self, e, n):
        return (1 - e) / 4

    def MN(self):
        array = []
        for i in range(len(self.Pc)):
            N = [self.N1(self.Pc[i][0], self.Pc[i][1]),
                 self.N2(self.Pc[i][0], self.Pc[i][1]),
                 self.N3(self.Pc[i][0], self.Pc[i][1]),
                 self.N4(self.Pc[i][0], self.Pc[i][1])]
            array.append(N)
        return  np.array(array)

    def MdNde(self):
        array = []
        for i in range(len(self.Pc)):
            N = [self.dN1e(self.Pc[i][0], self.Pc[i][1]),
                 self.dN2e(self.Pc[i][0], self.Pc[i][1]),
                 self.dN3e(self.Pc[i][0], self.Pc[i][1]),
                 self.dN4e(self.Pc[i][0], self.Pc[i][1])]
            array.append(N)
        return  np.array(array)


    def MdNdn(self):
        array = []
        for i in range(len(self.Pc)):
            N = [self.dN1n(self.Pc[i][0], self.Pc[i][1]),
                 self.dN2n(self.Pc[i][0], self.Pc[i][1]),
                 self.dN3n(self.Pc[i][0], self.Pc[i][1]),
                 self.dN4n(self.Pc[i][0], self.Pc[i][1])]
            array.append(N)
        return np.array(array)

