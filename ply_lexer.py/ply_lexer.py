import ply_lexer_specification
import ply.lex as lex
from tokken import Token

class Lexer:
    def __init__(self):
        self.lexer = lex.lex(module= ply_lexer_specification)
    
    def tokenize(self, code):
        self.lexer.input(code)
        tokens = []
        for token in self.lexer:
            tokens.append(Token(token.type, token.value, token.lineno))
        return tokens
