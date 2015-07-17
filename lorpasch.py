from collections import namedtuple
import re

import pandas

class Lorpasch:
    def __init__(self, *args, dim_prefix = '', fact_prefix = ''):
        '''
        Either a data frame or

        dimensions, facts
        '''
        self.dim_prefix = dim_prefix
        self.fact_prefix = fact_prefix
        if len(args) == 1:
            self.df, = args
            self.dimensions = [re.sub('^' + self.dim_prefix, '', c) for c in self.df.columns]
            self.facts = [re.sub('^' + self.fact_prefix, '', c) for c in self.df.columns]
        elif len(args) == 2:
            self.dimensions, self.facts = args
            columns = [self.dim_prefix + d for d in dimensions] + [self.fact_prefix + f for f in facts]
            self.df = pandas.DataFrame(columns = columns)
        else:
            raise TypeError('One argument or two arguments')

    def __repr__(self):
        return repr(self.df)

    def slice(self, dimension, value):
        return Lorpasch(self.df[getattr(self.df, self.dim_prefix + dimension) == value])

    def dice(self, dimension, *values):
        dfs = (self.slice(dimension, value).df for value in values)
        return Lorpasch(pandas.concat(dfs))


data = {
#   (dim1value, dim2value, ...): set(),
}
