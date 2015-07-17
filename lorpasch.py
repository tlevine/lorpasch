from collections import namedtuple
import re

import pandas

class Lorpasch:
    def __init__(self, *args, dim_prefix = 'dim_', fact_prefix = 'fact_'):
        '''
        Either a data frame or

        dimensions, facts
        '''
        self.dim_prefix = dim_prefix
        self.fact_prefix = fact_prefix
        if len(args) == 1:
            self.df, = args
            self.dimensions = [re.sub('^' + self.dim_prefix, '', c) for c in self.df.columns if c.startswith(self.dim_prefix)]
            self.facts = [re.sub('^' + self.fact_prefix, '', c) for c in self.df.columns if c.startswith(self.fact_prefix)]
        elif len(args) == 2:
            self.dimensions, self.facts = args
            columns = [self.dim_prefix + d for d in self.dimensions] + [self.fact_prefix + f for f in self.facts]
            self.df = pandas.DataFrame(columns = columns)
        else:
            raise TypeError('One argument or two arguments')

    def __repr__(self):
        return repr(self.df)

    def __iter__(self):
        return zip(*(self.df[self.fact_prefix + f] for f in self.facts))

    def rollup(self, func, *args, **kwargs):
        '''
        Aggregate all of the facts with the passed function.

        :param func: Function that takes a pandas column, or the string
            name of a pandas column method (sum, mean, quantile, &c)
        :rtype tuple:
        :returns: The aggregates, one per column

        The remaining arguments are passed to the function.

        '''
        if isinstance(func, str):
            def f(column):
                return getattr(column, func)(*args, **kwargs)
        else:
            def f(column):
                return func(column, *args, **kwargs)
        columns = (getattr(self.df, name) for name in self.df.columns)
        return tuple(map(f, columns))

    def insert(self, *args):
        rows, columns = self.df.shape
        if len(args) != columns:
            raise ValueError('You must pass %d arguments.' % columns)
        self.df.loc[rows + 1] = args

    def slice(self, dimension, value):
        return Lorpasch(self.df[getattr(self.df, self.dim_prefix + dimension) == value])

    def dice(self, dimension, *values):
        dfs = (self.slice(dimension, value).df for value in values)
        return Lorpasch(pandas.concat(dfs))

def example():
    p = Lorpasch(('year', 'month'), ('rainfall',))
    p.insert(2015, 1, 3.3)
    p.insert(2015, 2, 8.3)
    p.insert(2015, 3,21.3)
    p.insert(2015, 4,29.3)
    p.insert(2015, 5,23.3)
    p.insert(2015, 6,17.3)
    print(list(p.dice('month', 1, 5)))
    return p
