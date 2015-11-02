# geochains.py
# author: oral okan
# date: november 2, 2015
# modified: november 2, 2015

import re
from expander import Expander
from expander import SubstitutionRule
from geodb import GeoIPDBMaxMind

PATTERN=r'\[.*?\]'      # using non-greedy qualifier

class GeochainsSubstitutionRule(SubstitutionRule):
    def values_for_match(self, matched):
        try:
            query_type = re.compile(r'\[.*?:').search(matched).group()[1:-1].strip()
            query_list = re.compile(r':.*?\]').search(matched).group()[1:-1].strip().split(',')
        except AttributeError:
            print "ERROR: Malformed pattern: {}".format(matched)
            raise SystemExit
        
        if query_type == 'CN':
            return self.country_search(query_list)

        elif query_type == 'AS':
            return self.country_search(query_list)

        else:
            print "ERROR: Malformed pattern: {}".format(matched)
            raise SystemExit

    def country_search(self, patterns):
        return ["IPs of countries:{}".format(','.join(patterns))]

    def as_search(self, patterns):
        return ["IPs of ASs:{}".format(','.join(patterns))]


class Geochains:

    def __init__(self):
        self.pattern = PATTERN
        self.sub_rule = GeochainsSubstitutionRule()
        expander = Expander(self.pattern, self.sub_rule)

        sample_input = \
r'''
[CN:turkey,usa] 
[AS:13,421]
'''

        output = expander.expand(sample_input)

        self.geodb = GeoIPDBMaxMind()
        print self.geodb.search_as_name(["univer"])

Geochains()

