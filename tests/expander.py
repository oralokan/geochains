# test the expander

import unittest
from src import expander

def sample_callback_1(matched):
    if matched == r'[D]':
        return ['1','2']

def sample_callback_2(matched):
    if matched == r'[D]':
        return ['1','2']

    if matched == r'[L]':
        return ['a', 'b']


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.expander = expander.Expander()

    def test_single_expansion(self):
        sample_input = r'[D] is a digit'
        self.expander.pattern='\[D\]' # these ones need the escapes
        self.expander.substitute_callback = sample_callback_1
        output = self.expander._expand_line(sample_input)
        expected_output = '1 is a digit\n2 is a digit'
        self.assertEqual(output, expected_output)

    def test_double_expansion(self):
        sample_input = r'[D] + [D]'
        self.expander.pattern='\[D\]'
        self.expander.substitute_callback = sample_callback_1
        output = self.expander._expand_line(sample_input)
        expected_output = \
'''1 + 1
1 + 2
2 + 1
2 + 2'''

        self.assertEqual(len(output.split('\n')), len(expected_output.split('\n')))
        self.assertEqual(set(output.split('\n')), set(expected_output.split('\n')))

    def test_conditional_callback(self):
        sample_input = r'[D] + [L]'
        self.expander.pattern='\[.\]'
        self.expander.substitute_callback = sample_callback_2
        output = self.expander._expand_line(sample_input)
        expected_output = \
'''1 + a
1 + b
2 + a
2 + b'''

        self.assertEqual(len(output.split('\n')), len(expected_output.split('\n')))
        self.assertEqual(set(output.split('\n')), set(expected_output.split('\n')))

    def test_example_input(self):
        sample_input = \
r'''[D] is a digit, '[L]' is a letter
I said, '[L]' is a letter!!!
And this line stays the same'''
        self.expander.pattern='\[.\]'
        self.expander.substitute_callback = sample_callback_2
        output = self.expander.expand(sample_input)
        expected_output = \
'''1 is a digit, 'a' is a letter
1 is a digit, 'b' is a letter
2 is a digit, 'a' is a letter
2 is a digit, 'b' is a letter
I said, 'a' is a letter!!!
I said, 'b' is a letter!!!
And this line stays the same'''

        self.assertEqual(len(output.split('\n')), len(expected_output.split('\n')))
        self.assertEqual(set(output.split('\n')), set(expected_output.split('\n')))
        self.assertEqual(output.split('\n')[-1], expected_output.split('\n')[-1])


if __name__ == '__main__':
    unittest.main()
