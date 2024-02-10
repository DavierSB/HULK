from get_next_token import *

code = None
with open('prueba_long.txt', 'r') as f_in:
    code = f_in.read()

lex = lexer(code)
while lex.idx < len(code):
    tok = lex.get_next_token()
    print(tok)