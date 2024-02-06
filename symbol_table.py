from abc import ABC

class token:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value

class symbol(ABC):
    def __init__(self, id=None, type=None, value=None, priority=None, associativity=None) -> None:
        self.type = type
        self.id = id
        self.value = value
        self.priority = priority
        self.associativity = associativity
        self.hasNext = False    

symbol_table = {}

symbol_table['('] = symbol('(', 'sep', None, 1 , None)
symbol_table[')'] = symbol(')', 'sep', None, 1 , None)
symbol_table['['] = symbol('[', 'sep', None, 1 , None)
symbol_table[']'] = symbol(']', 'sep', None, 1 , None)
symbol_table['{'] = symbol('{', 'sep', None, 1 , None)
symbol_table['}'] = symbol('}', 'sep', None, 1 , None)
symbol_table[';'] = symbol(';', 'sep', None, 1 , None)

symbol_table['+'] = symbol('+', 'opp', None, 20, 'left')
symbol_table['-'] = symbol('-', 'opp', None, 20, 'left')
symbol_table['*'] = symbol('*', 'opp', None, 10, 'left')
symbol_table['/'] = symbol('/', 'opp', None, 10, 'left')
symbol_table['^'] = symbol('^', 'opp', None, 5 , 'left')

symbol_table['='] = symbol('=', 'opp', None, 30, None)
symbol_table['<'] = symbol('<', 'opp', None, 25, None)
symbol_table['>'] = symbol('>', 'opp', None, 25, None)

symbol_table[':='] = symbol(':=', 'opp', None, 30, None)
symbol_table['<='] = symbol('<=', 'opp', None, 25, None)
symbol_table['>='] = symbol('>=', 'opp', None, 25, None)
symbol_table['=='] = symbol('==', 'opp', None, 25, None)
