from collections import namedtuple

class Lorpasch(dict):
    def __init__(self, dimensions):
        '''
        Takes a list of dimension names
        '''
        self.dimensions = 
        self.Pixel = namedtuple('Pixel', dimensions)

    def insert(self, key, value):
        if len(key) != len(self.dimensions):
            raise KeyError('Not a valid key')

        if hasattr(key, 'items'):
            pixel = self.Pixel(**key)
        else:
            pixel = self.Pixel(*key)

        if pixel not in self:
            self[pixel] = set()
        self[pixel].add(pointer)

def lorpasch(*dimensions):


data = {
#   (dim1value, dim2value, ...): set(),
}
