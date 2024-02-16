import unittest

import sys
import os

sys.path.insert(0, os.getcwd() + '/lexer')
from get_next_token import *

class LexerTest(unittest.TestCase):
    def test_get_next_token(self):
        code = None
        with open('./tests/data/prueba_short.txt', 'r') as f_in:
            code = f_in.read()
        lex = lexer(code)
        while lex.idx < len(code):
            tok = lex.get_next_token()
            print(tok)

if __name__ == '__main__':
    unittest.main()