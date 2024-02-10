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
    def __init__(self, args) -> None:
        self.language, self.reserved_words = define_language()
        self.args = args
        self.line = 1
        self.idx = 0
    
    def get_next_token(self):
        if self.idx == len(self.args): return EOFError("There are no more tokens to read")
        name = 'ignore'
        while name == 'ignore':
            lexeme, name, line, k = self.language.match(self.args, self.idx, self.line)
            self.line = line
            self.idx = k
        return self.create_token(lexeme, name, line)
    
    def create_token(self, lexeme, name, line):
        if self.reserved_words.keys().__contains__(lexeme):
            return token(lexeme, self.reserved_words[lexeme], line)
        return token(lexeme, name, line)
    