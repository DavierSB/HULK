from typing import List, Dict, Set
from cmp.pycompiler import Grammar, Production, Symbol, Sentence

def calculate_firsts_for_symbols(grammar : Grammar) -> None:
    initialize_firsts(grammar)
    changed = True
    while changed:
        changed = False
        for production in grammar.Productions:
            changed = augment_grammar_firsts(grammar, production) or changed

def initialize_firsts(grammar : Grammar) -> None:
    grammar.firsts = {}
    for t in grammar.terminals:
        grammar.firsts[t] = set([t])
    for nt in grammar.nonTerminals:
        grammar.firsts[nt] = set()

def augment_grammar_firsts(grammar: Grammar, production : Production) -> bool:
    n_of_elements_before_updating = len(grammar.firsts[production.Left])
    grammar.firsts[production.Left].update(calculate_firsts_for_sentence(production.Right, grammar))
    return len(grammar.firsts[production.Left]) > n_of_elements_before_updating

def calculate_firsts_for_sentence(sentence : Sentence, grammar : Grammar) -> Set[Symbol]:
    all_contain_epsilon = True
    firsts_set = set()
    for symbol in sentence:
        all_contain_epsilon = grammar.Epsilon in grammar.firsts[symbol]
        firsts_set.update(grammar.firsts[symbol])
        if not all_contain_epsilon:
            break
    if all_contain_epsilon:
        firsts_set.add(grammar.Epsilon)
    return firsts_set