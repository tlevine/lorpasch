from collections import namedtuple

class Lorpasch(dict):
    def __init__(self, *dimensions):
        self.Pixel = namedtuple('Pixel', dimensions)
    def insert(self):
        pass
        

data = {
#   (dim1value, dim2value, ...): set(),
}
