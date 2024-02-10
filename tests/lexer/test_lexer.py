import unittest


import sys
sys.path.insert(0, '//home/chavely/Documents/start up/compiler/test 1/hulk test/lexer')

from get_next_token import *

class LexerTest(unittest.TestCase):
    def test_get_next_token(self):
        code = None
        with open('./tests/lexer/prueba_short.txt', 'r') as f_in:
            code = f_in.read()
        lex = lexer(code)
        while lex.idx < len(code):
            tok = lex.get_next_token()

if __name__ == '__main__':
    unittest.main()