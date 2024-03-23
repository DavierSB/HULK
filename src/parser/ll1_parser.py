from firsts_and_follows import compute_firsts, compute_follows
from stack import Stack
def build_parsing_table(G, firsts, follows):
    table = {}
    for production in G.Productions:
        X = production.Left
        alpha = production.Right
        has_epsilon = True
        if not alpha.IsEpsilon:
            has_epsilon = False
            for terminal in firsts[alpha]:
                if terminal.IsEpsilon:
                    has_epsilon = True
                    continue
                table[X, terminal] = [production]
        if has_epsilon:
            for terminal in follows[X]:
                table[X, terminal] = [production]

    return table

def metodo_predictivo_no_recursivo(G, table=None, firsts=None, follows=None):
    if table is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        table = build_parsing_table(G, firsts, follows)
    
    def parser(w):
        # w ends with $ (G.EOF)
        stack = Stack()
        stack.push(G.EOF)
        stack.push(G.startSymbol)
        cursor = 0
        output = []
        
        while True:
            top = stack.pop()
            a = w[cursor]
            if top.IsTerminal:
                if a == top:
                    cursor += 1
                if a == G.EOF:
                    break
                continue
            production = table[top, a][0]
            output.append(production)
            if not production.IsEpsilon:
                for symbol in reversed(production.Right):
                    stack.push(symbol)
        return output
    
    return parser