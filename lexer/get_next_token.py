from automata import *
from specifications import *

class token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line
    
    def __str__(self):
        return "( " + self.type + "   " + str(self.value) + "   in line " + str(self.line) + " )"

class lexer:
    def __init__(self, args) -> None:
        self.language = define_language(automata())
        self.args = args
        self.line = 1
        self.idx = 0
    
    def get_next_token(self):
        if self.idx == len(self.args): return EOFError("There are no more tokens to read")
        type, value, line, k = self.language.match(self.args, self.idx, self.line)
        self.line = line
        self.idx = k
        
        return token(type, value, line)