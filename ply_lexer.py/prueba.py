import ply_lexer

lex = ply_lexer.Lexer()

code = None
with open('prueba_short.txt', 'r') as f_in:
    code = f_in.read()
tokens = lex.tokenize(code)
for token in tokens:
    print(token)