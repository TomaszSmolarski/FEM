
class GlobalData:
    def __init__(self, H, W, nH, nW):
        self.H = H
        self.W = W
        self.nH = nH
        self.nW = nW
        self.nN = nH * nW
        self.nE = (nW - 1) * (nH - 1)

