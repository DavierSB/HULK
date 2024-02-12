
class symbol:
    def __init__(self, lexeme, name) -> None:
        self.lexeme = lexeme
        self.name = name
        self.value = self.get_value(lexeme)
    
    

class symbol_table:
    def __init__(self, tokens) -> None:
        self.name = {}
        self.value = {}
        for t in tokens: self.add_token(t)
            
    def add_token(self, token):
        self.name[token.lexeme] = token.name
        self.value[token.lexeme] = self.get_value(token)
        
    
    def get_value(self, lexeme):
        pass
    