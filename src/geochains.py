# geochains.py
# author: oral okan
# date: november 2, 2015
# modified: november 2, 2015

from expander import Expander
from substitution_rule import SubstitutionRule 

PATTERN=r'\[.*?\]'      # using non-greedy qualifier

class GeochainsSubstitutionRule(SubstitutionRule):
    def values_for_match(self, matched):
        print matched
        if matched == r'[D]':
            return ['1','2']

        if matched == r'[L]':
            return ['a', 'b']



class Geochains:

    def __init__(self):
        self.pattern = PATTERN
        self.sub_rule = GeochainsSubstitutionRule()
        expander = Expander(self.pattern, self.sub_rule)

        print expander
        print expander.pattern
        print expander.substitution_rule

        sample_input = \
r'''[D] is a digit, '[L]' is a letter
Again, '[L]' is a letter
And this line stays the same'''

        output = expander.expand(sample_input)

        print output

Geochains()

