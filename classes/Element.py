
from classes.Node import Node

class Element:
    def __init__(self, id: int, nodes: [Node]):
        self.__id = id
        self.__nodes = nodes
        self.__edges_with_bc = self.__edges_with_bc()

    def __str__(self):
        return f"Element: [id: {self.__id}; nodes: {self.__nodes}" \
               f"; walls_with_bc: {self.__edges_with_bc}]"

    def __repr__(self):
        return f"Element: [id: {self.__id}; nodes: {self.__nodes}" \
               f"; wall_numbers: {self.__edges_with_bc}]"

    @property
    def id(self):
        return self.__id

    @property
    def nodes(self):
        return self.__nodes

    @property
    def walls_with_bc(self):
        return self.__edges_with_bc

    def __edges_with_bc(self):
        edges_with_bc = {}
        for i in range(4):
            if self.nodes[i].bc and self.nodes[(i + 1) % 4].bc:
                edges_with_bc[i] = [self.nodes[i], self.nodes[(i + 1) % 4]]
        return edges_with_bc
