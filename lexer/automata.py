class Transition:
    def __init__(self, dest_node, condition, to_write):
        self.dest_node = dest_node
        self.condition = condition
        self.to_write = to_write

class Node:
    def __init__(self, idx) -> None:
        self.idx = idx
        self.transitions = []
        self.name = None
        self.output = False

class Automata:
    def __init__(self) -> None:
        self.start_node = Node(0)
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