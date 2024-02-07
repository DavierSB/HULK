from abc import ABC

class symbol(ABC):
    def __init__(self, id=None, type=None, priority=None, associativity=None) -> None:
        self.type = type
        self.id = id
        self.priority = priority
        self.associativity = associativity
        self.hasNext = False    

class token:
    def __init__(self, symbol: symbol, value) -> None:
        self.value = value
        self.symbol = symbol

symbol_table = {}

symbol_table['('] = symbol('(', 'sep', 1 , None)
symbol_table[')'] = symbol(')', 'sep', 1 , None)
symbol_table['['] = symbol('[', 'sep', 1 , None)
symbol_table[']'] = symbol(']', 'sep', 1 , None)
symbol_table['{'] = symbol('{', 'sep', 1 , None)
symbol_table['}'] = symbol('}', 'sep', 1 , None)
symbol_table[';'] = symbol(';', 'sep', 1 , None)

symbol_table['+'] = symbol('+', 'opp', 20, 'left')
symbol_table['-'] = symbol('-', 'opp', 20, 'left')
symbol_table['*'] = symbol('*', 'opp', 10, 'left')
symbol_table['/'] = symbol('/', 'opp', 10, 'left')
symbol_table['^'] = symbol('^', 'opp', 5 , 'left')

symbol_table['='] = symbol('=', 'opp', 30, None)
symbol_table['<'] = symbol('<', 'opp', 25, None)
symbol_table['>'] = symbol('>', 'opp', 25, None)

symbol_table[':='] = symbol(':=', 'opp', 30, None)
symbol_table['<='] = symbol('<=', 'opp', 25, None)
symbol_table['>='] = symbol('>=', 'opp', 25, None)
symbol_table['=='] = symbol('==', 'opp', 25, None)
