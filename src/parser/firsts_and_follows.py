import os
import sys
sys.path.insert(0, os.path.dirname(os.getcwd()))
from cmp.utils import ContainerSet

def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
    
    if not alpha_is_epsilon:
        for symbol in alpha:
            first_of_symbol = firsts[symbol]
            first_alpha.update(first_of_symbol)
            if not(first_of_symbol.contains_epsilon):
                return first_alpha
    
    first_alpha.set_epsilon()
    return first_alpha


def compute_firsts(G):
    firsts = {}
    change = True
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            first_X = firsts[X]
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            local_first = compute_local_first(firsts, alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
    
    return firsts

def compute_follows(G, firsts):
    follows = { }
    change = True
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            # X -> zeta Y beta
            # First(beta) - { epsilon } subset of Follow(Y)
            # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
            for i in range(len(alpha)):
                Y = alpha[i]
                if Y.IsNonTerminal:
                    zeta = alpha[:i]
                    beta = alpha[i+1:]
                    if len(beta) > 0:
                        if not (beta in firsts):
                            firsts[beta] = compute_local_first(firsts, beta)
                        firsts_of_beta = firsts[beta]
                        change |= follows[Y].update(firsts_of_beta)
                    else:
                        firsts_of_beta = ContainerSet(contains_epsilon= True)
                    if firsts_of_beta.contains_epsilon:
                        change |= follows[Y].update(follows[X])

    return follows