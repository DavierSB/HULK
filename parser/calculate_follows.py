from typing import List, Dict, Set
from cmp.pycompiler import Grammar, Production, Symbol, Sentence
from calculate_firsts import calculate_firsts_for_sentence

def calculate_follows(grammar : Grammar):
    initialize_follows(grammar)
    changed = True
    while changed:
        changed = False
        for production in grammar.Productions:
            for i in range(len(production.Right)):
                if production.Right[i].IsNonTerminal:
                    changed = augment_grammar_follows(grammar, production, i) or changed
                
def initialize_follows(grammar : Grammar):
    grammar.follows = {}
    for nt in grammar.nonTerminals:
        grammar.follows[nt] = set()
    grammar.follows[grammar.startSymbol].add(grammar.EOF)

def augment_grammar_follows(grammar : Grammar, production : Production, idx : int) -> bool:
    sentence = production.Right
    nonTerminal = sentence[idx]
    chunk = sentence[idx + 1:]
    n_of_elements_before_updating = len(grammar.follows[nonTerminal])
    firsts = calculate_firsts_for_sentence(chunk, grammar)  #Si chunk == [], epsilo pertenece a firsts_for_sentence
    if grammar.Epsilon in firsts:
        grammar.follows[nonTerminal].update(grammar.follows[production.Left])
        firsts.remove(grammar.Epsilon)
    grammar.follows[nonTerminal].update(firsts)
    return len(grammar.follows[nonTerminal]) > n_of_elements_before_updating