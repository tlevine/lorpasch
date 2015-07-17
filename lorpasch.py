from collections import namedtuple
import re

import pandas

class Lorpasch:
    def __init__(self, *args):
        '''
        Either a data frame or

        dimensions, facts
        '''
        if len(args) == 1:
            self.df, = args
            self.dimensions = [re.sub(r'^dim_', '', c) for c in self.df.columns]
            self.facts = [re.sub(r'^fact_', '', c) for c in self.df.columns]
        elif len(args) == 2:
            self.dimensions, self.facts = args
            columns = ['dim_' + d for d in dimensions] + ['fact_' + f for f in facts]
            self.df = pandas.DataFrame(columns = columns)
        else:
            raise TypeError('One argument or two arguments')

    def slice(self, dimension, value):
        df[getattr(df, 'aoeu') == 'x']


data = {
#   (dim1value, dim2value, ...): set(),
}
