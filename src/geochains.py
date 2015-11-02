# geochains.py
# author: oral okan
# date: november 2, 2015
# modified: november 2, 2015

from expander import Expander

PATTERN=r'\[.*\]'



class Geochains:

    def sub_fn(self, matched):
        if matched == r'[D]':
            return ['1','2']

        if matched == r'[L]':
            return ['a', 'b']

    def __init__(self):
        self.pattern = PATTERN
        expander = Expander(self.pattern, self.sub_fn)

        sample_input = \
r'''[D] is a digit, '[L]' is a letter
Again, '[L]' is a letter
And this line stays the same'''

        output = expander.expand(sample_input)

        print output

Geochains()

