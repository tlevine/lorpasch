from collections import namedtuple
import re
from functools import reduce, partial

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
        '''
        Destructive, not on purpose

        :rtype NoneType:
        :returns: None
        '''
        rows, columns = self.df.shape
        if len(args) != columns:
            raise ValueError('You must pass %d arguments.' % columns)
        new = Lorpasch(self.df)
        new.df.loc[rows + 1] = args # destructive, bad
        return new

    def slice(self, dimension, value):
        return self.dice(dimension, value)

    def _slice(self, dimension, value):
        return getattr(self.df, self.dim_prefix + dimension) == value

    def dice(self, dimension, *values):
        f = partial(self._slice, dimension)
        def g(left, right):
            return left | right
        return Lorpasch(self.df[reduce(g, map(f, values))])

