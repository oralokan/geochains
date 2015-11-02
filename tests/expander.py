# test the expander

import unittest
from src.expander import Expander
from src.substitution_rule import SubstitutionRule 

class MySubstitutionRule(SubstitutionRule):
    def values_for_match(self, matched):
        if matched == r'[D]':
            return ['1','2']

        if matched == r'[L]':
            return ['a', 'b']


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.expander = Expander(r'\[.\]', MySubstitutionRule())

    def test_single_expansion(self):
        '''
        input:
        '[D] is a digit'

        output:
        '1 is a digit'
        '2 is a digit'
        '''
        sample_input = r'[D] is a digit'
        expected_output = '1 is a digit\n2 is a digit'
        output = self.expander.expand(sample_input)
        self.assertEqual(output, expected_output)

    def test_double_expansion(self):
        '''
        input:
        '[D] + [D]'

        output: (order not important)
        '1 + 1'
        '1 + 2'
        '2 + 1'
        '2 + 2'
        '''
        sample_input = r'[D] + [D]'
        output = self.expander.expand(sample_input)
        expected_output = \
'''1 + 1
1 + 2
2 + 1
2 + 2'''
        self.assertEqual(len(output.split('\n')), len(expected_output.split('\n')))
        self.assertEqual(set(output.split('\n')), set(expected_output.split('\n')))

    def test_conditional_callback(self):
        '''
        input:
        '[D] + [L]'

        output: (order not important)
        '1 + a'
        '1 + b'
        '2 + a'
        '2 + b'
        '''
        sample_input = r'[D] + [L]'
        output = self.expander.expand(sample_input)
        expected_output = \
'''1 + a
1 + b
2 + a
2 + b'''
        self.assertEqual(len(output.split('\n')), len(expected_output.split('\n')))
        self.assertEqual(set(output.split('\n')), set(expected_output.split('\n')))

    def test_multiline_input(self):
        '''
        input:
        '[D] is a digit, '[L]' is a letter'
        'Again, '[L]' is a letter'
        'And this line stays the same'

        output: order amongst lines from same template not important
        '1 is a digit, 'a' is a letter'
        '1 is a digit, 'b' is a letter'
        '2 is a digit, 'a' is a letter'
        '2 is a digit, 'b' is a letter'
        'Again, 'a' is a letter'
        'Again, 'b' is a letter'
        'And this line stays the same'
        '''
        sample_input = \
r'''[D] is a digit, '[L]' is a letter
Again, '[L]' is a letter
And this line stays the same'''
        output = self.expander.expand(sample_input)
        expected_output = \
'''1 is a digit, 'a' is a letter
1 is a digit, 'b' is a letter
2 is a digit, 'a' is a letter
2 is a digit, 'b' is a letter
Again, 'a' is a letter
Again, 'b' is a letter
And this line stays the same'''

        self.assertEqual(len(output.split('\n')), len(expected_output.split('\n')))
        self.assertEqual(set(output.split('\n')), set(expected_output.split('\n')))
        self.assertEqual(output.split('\n')[-1], expected_output.split('\n')[-1])


if __name__ == '__main__':
    unittest.main()
