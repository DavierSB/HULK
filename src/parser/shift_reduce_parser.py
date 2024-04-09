import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.pycompiler import Terminal
class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w, get_shift_reduce= False, show= False):
        stack = [ 0 ]
        cursor = 0
        output = []
        if get_shift_reduce:
            operations = []
        
        while True:
            state = stack[-1]
            if isinstance(w[cursor], Terminal):
                lookahead = w[cursor]
            else:
                lookahead = w[cursor].token_type
            
            try:
                action, tag = self.action[state, lookahead]
            except:
                raise Exception("ERROR line " + str(w[cursor].line) + ": Unexpected " + w[cursor].lex + " found")
            if get_shift_reduce:
                operations.append(action)
            match action:
                case self.SHIFT:
                    stack.append(tag)
                    if show:
                        print("SHIFT")
                    cursor += 1
                case self.REDUCE:
                    production = tag
                    for i in range(len(production.Right)):
                        stack.pop()
                    state = stack[-1]
                    stack.append(self.goto[state, production.Left])
                    output.append(production)
                    if show:
                        print(production)
                        input()
                case self.OK:
                    if get_shift_reduce:
                        return output, operations[:-1]# lo del -1 es un parche, para no devolver la accion OK
                    else:
                        return output