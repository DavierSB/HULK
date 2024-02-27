import sys
import os
current_dir = os.getcwd()
sys.path.insert(0, current_dir)
from cmp.pycompiler import Grammar
from grammars import Grammar_LL, Grammar_LR
from cmp.languages import BasicHulk
from cmp.utils import pprint, inspect

def grammar_LR():
    G = Grammar_LR()
    E = G.NonTerminal('E', True)
    T = G.NonTerminal('T')
    plus, star, opar, cpar, num = G.Terminals('+ * ( ) num')
    
    E %= T + plus + E | T
    T %= num + star + T | num | opar + E + cpar

    return G

def grammar_LL():
    G = Grammar_LL()
    E = G.NonTerminal('E', True)
    T,F,X,Y = G.NonTerminals('T F X Y')
    plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')
    
    E %= T + X
    X %= plus + T + X | minus + T + X | G.Epsilon
    T %= F + Y
    Y %= star + F + Y | div + F + Y | G.Epsilon
    F %= num | opar + E + cpar

    return (G, [num, star, opar, num, plus, num, cpar])

grammar, ecuation = grammar_LL()
grammar.initialize()