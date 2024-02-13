from automata import *
from specifications import *

class token:
    def __init__(self, lexeme, name, line):
        self.lexeme = lexeme
        self.name = name
        self.line = line
    
    def __str__(self):
        return "( " + self.lexeme + "   " + str(self.name) + "   in line " + str(self.line) + " )"

class lexer:
    def __init__(self, code) -> None:
        self.language, self.reserved_words = define_language()
        self.code = code
        self.line = 1
        self.idx = 0
    
    def get_next_token(self):
        if self.idx == len(self.code): return EOFError("There are no more tokens to read")
        name = 'IGNORE'
        while name == 'IGNORE':
            lexeme, name, self.line, self.idx = self.language.match(self.code, self.idx, self.line)
        return self.create_token(lexeme, name, self.line)
    
    def create_token(self, lexeme, name, line):
        return token(lexeme, self.reserved_words.get(lexeme, name), line)