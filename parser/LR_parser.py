import stack
from typing import List, Dict, Set
from cmp.pycompiler import Grammar, Production, Symbol, Sentence
from calculate_firsts import calculate_firsts_for_symbols, firsts_for_sentence
from calculate_follows import calculate_follows

def parse(code : str, grammar : Grammar) -> List[Production]:
    actions, goto = get_tables(grammar)
    stack = stack.Stack()
    idx = 0
    productions = []
    while True:
        state = stack.peek()
        symbol = code[idx]
        current_action = actions[state, symbol]
        if current_action.is_shift():
            stack.push(current_action.next_state)
            idx = idx + 1
            continue
        if current_action.is_reduce():
            current_production = current_action.production
            productions.append(current_production)
            for _ in range(len(current_production.Right)):
                stack.pop()
            stack.push(goto(stack.peek(), current_production.Left))
            continue
        if current_action.is_error():
            pass
        if current_action.is_accept():
            productions.reverse()
            return productions

def get_tables(grammar : Grammar):
    augment_gramatic(grammar)
    calculate_firsts_for_symbols(grammar)
    calculate_follows(grammar)

def augment_gramatic(grammar : Grammar):
    E = grammar.startSymbol
    grammar.startSymbol = None
    foolE = grammar.NonTerminal('E\'', True)
    foolE %= E