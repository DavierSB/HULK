import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.pycompiler import Item
from cmp.automata import State
from shift_reduce_parser import ShiftReduceParser
from firsts_and_follows import compute_firsts, compute_follows

def build_LR0_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)
    automaton = State(start_item, True)
    pending = [ start_item ]
    visited = { start_item: automaton }

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue

        next_item = current_item.NextItem()
        if not next_item in visited:
            pending.append(next_item)
            next_state = State(next_item, True)
            visited[next_item] = next_state
        else:
            next_state = visited[next_item]
        next_state_through_regular_transition = next_state
        
        next_symbol = current_item.NextSymbol
        states_through_epsilon_transitions = []
        if next_symbol.IsNonTerminal:
            for production in next_symbol.productions:
                next_item = Item(production, 0)
                if not next_item in visited:
                    pending.append(next_item)
                    next_state = State(next_item, True)
                    visited[next_item] = next_state
                else:
                    next_state = visited[next_item]
                states_through_epsilon_transitions.append(next_state)

        current_state = visited[current_item]
        current_state.add_transition(next_symbol.Name, next_state_through_regular_transition)
        for epsilon_transition in states_through_epsilon_transitions:
            current_state.add_epsilon_transition(epsilon_transition)
    
    return automaton


class SLR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                if item.IsReduceItem:
                    head = item.production.Left
                    if head == G.startSymbol:
                        SLR1Parser._register(self.action, (idx, G.EOF), (self.OK, None))
                    else:
                        for symbol in follows[head]:
                            SLR1Parser._register(self.action, (idx, symbol), (self.REDUCE, item.production))
                    continue
                next_symbol = item.NextSymbol
                next_node = node[next_symbol.Name][0].idx
                if next_symbol.IsTerminal:
                    SLR1Parser._register(self.action, (idx, next_symbol), (self.SHIFT, next_node))
                else:
                    SLR1Parser._register(self.goto, (idx, next_symbol), next_node)
    @staticmethod
    def _register(table, key, value):
        assert ((key not in table) or (table[key] == value)), 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value