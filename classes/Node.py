
class Node:

    def __init__(self, id: int, temp=0.0, x=0.0, y=0.0, bc: bool=False):
        self.temp = temp
        self.x = x
        self.y = y
        self.bc = bc
        self.id = id

    def __str__(self):
        return "[nr:%s,x:%s,y:%s,temp:%s,bc:%s]" % (self.id, format(self.x, '.3f'), format(self.y, '.3f'), self.temp, self.bc)

    def __repr__(self):
        return "[nr:%s,x:%s,y:%s,temp:%s,bc:%s]" % (self.id, format(self.x, '.3f'), format(self.y, '.3f'), self.temp, self.bc)

