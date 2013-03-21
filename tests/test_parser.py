import unittest
from connive.parser import *

class TestTokenize(unittest.TestCase):
    def test_tokenize(self):
        expected = ['(', 'expression', ')']
        actual = tokenize('(expression)')
        self.assertEquals(actual, expected)
    
    def test_nested_tokens(self):
        expected = ['(', 'x', '(', 'y', 'z', ')', ')']
        actual = tokenize('(x (y z))')
        self.assertEquals(actual, expected)
    

class TestTransform(unittest.TestCase):
    def test_empty_transform(self):
        with self.assertRaises(SyntaxError):
            transform([])

    def test_invalid_first_token(self):
        with self.assertRaises(SyntaxError):
            transform([')', '(', ')'])

    def test_numeric_atoms(self):
        expected = [1, 5, 8]
        actual = transform(['(', '1', '5', '8', ')'])
        self.assertEquals(actual, expected)

    def test_symbolic_atoms(self):
        expected = ["fubar", 'atlas']
        actual = transform(['(', 'fubar', 'atlas', ')'])
        self.assertEquals(actual, expected)

