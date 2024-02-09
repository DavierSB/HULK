class node:
    def __init__(self) -> None:
        self.next = []
        self.cond = []
        self.write = []
        self.type = None
        self.output = False
        
    def add_next(self, node, cond, write):
        self.next.append(node)
        self.cond.append(cond)
        self.write.append(write)

class automata:
    def __init__(self) -> None:
        self.start_node = node()
        self.nodes = [self.start_node]

    def add_node(self, node):
        self.nodes.append(node)
        
    def add_transition(self, i, j, cond, write):
        self.nodes[i].add_next(self.nodes[j], cond, write)
    
    def set_output(self, idx, type):
        self.nodes[idx].output = True
        self.nodes[idx].type = type

    def match(self, args, idx, line):
        act = self.start_node; flag = True; k = 0; l = line; token = ''
        for i in range(idx, len(args)):
            if not flag: break
            flag = False
            for j in range(len(act.cond)):
                if act.cond[j](args[i]):
                    if act.write[j]:
                        token = token + args[i]
                    act = act.next[j]
                    flag = True; k=k+1
                    if args[i] == '\n': l=l+1
                    break
        if act.output: return act.type, token, l, idx+k
        else:
            value =  args[idx, idx+k]
            return 'undefined', value, l, idx+k

