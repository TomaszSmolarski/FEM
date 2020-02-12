class Node:

    def __init__(self, id: int, temp: float = 0.0, x: float = 0.0, y: float = 0.0, bc: bool = False):
        self.__temp = temp
        self.__x = x
        self.__y = y
        self.__bc = bc
        self.__id = id

    def __str__(self):
        return f"Node: [id: {self.__id}, x: {self.__x:.3f}, y: {self.__y:.3f}, temp: {self.__temp:.3f}, BC: {self.__bc}]"

    def __repr__(self):
        return f"Node: [id: {self.__id}, x: {self.__x:.3f}, y: {self.__y:.3f}, temp: {self.__temp:.3f}, BC: {self.__bc}]"

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def temp(self):
        return self.__temp

    @property
    def bc(self):
        return self.__bc

    @property
    def id(self):
        return self.__id

    @temp.setter
    def temp(self, value):
        self.__temp = value
