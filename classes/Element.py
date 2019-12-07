from classes.UniversalElement import UniversalElement as ue
import numpy as np
from classes.Node import Node


class Element:
    def __init__(self, id: int, nodes: [Node], wall_numbers: [], wall_amount=None):
        self.id = id
        self.nodes = nodes
        self.wall_amount = wall_amount
        self.wall_numbers = wall_numbers

    def __str__(self):
        return "[id:%s,nodes:%s,wall_amount:%s,wall_numbers:%s]\n" % (self.id, self.nodes, self.wall_amount, self.wall_numbers)

    def __repr__(self):
        return "[id:%s,nodes:%s,wall_amount:%s,wall_numbers:%s]\n" % (self.id, self.nodes, self.wall_amount, self.wall_numbers)
