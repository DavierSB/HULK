from transition import Transition
class node:
    def __init__(self) -> None:
        self.transitions = []
        self.name = None
        self.output = False

class automata:
    def __init__(self) -> None:
        self.start_node = node()
        self.nodes = [self.start_node]

    def add_node(self, node):
        self.nodes.append(node)
        
    def add_transition(self, i, j, cond, write = True):
        self.nodes[i].transitions.append(Transition(self.nodes[j], cond, write))
    
    def set_output(self, idx, name):
        self.nodes[idx].output = True
        self.nodes[idx].name = name

    def match(self, code, idx, line):
        act = self.start_node; valid_state = True; k = 0; lexeme = ''
        for c in code[idx:]:
            if not valid_state: break
            valid_state = False
            for trans in act.transitions:
                if trans.condition(c):
                    if trans.to_write:
                        lexeme = lexeme + c
                    act = trans.dest_node
                    valid_state = True; k=k+1
                    if c == '\n': line=line+1
                    break
        if act.output: return lexeme, act.name, line, idx+k
        else:
            lexeme =  code[idx, idx+k]
            return lexeme, 'UNDEFINED', line, idx+k