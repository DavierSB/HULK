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

    def __call__(self, w, get_shift_reduce= False):
        stack = [ 0 ]
        cursor = 0
        output = []
        if get_shift_reduce:
            operations = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
                
            # Your code here!!! (Detect error)
            
            action, tag = self.action[state, lookahead]
            if get_shift_reduce:
                operations.append(action)
            match action:
                case self.SHIFT:
                    stack.append(tag)
                    cursor += 1
                case self.REDUCE:
                    production = tag
                    for i in range(len(production.Right)):
                        stack.pop()
                    state = stack[-1]
                    stack.append(self.goto[state, production.Left])
                    output.append(production)
                case self.OK:
                    if get_shift_reduce:
                        return output, operations[:-1]# lo del -1 es un parche, para no devolver la accion OK
                    else:
                        return output