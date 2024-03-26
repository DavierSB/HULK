import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/automata')
sys.path.insert(0, current_dir + '/src/parser')
from automata.dfa import DFA
from automata.automata_utils import automata_closure, automata_concatenation, automata_union
from cmp.ast import AtomicNode, UnaryNode, BinaryNode
from cmp.pycompiler import Grammar
from cmp.utils import Token

class EpsilonNode(AtomicNode):
    def evaluate(self):
        return DFA(states= 1, finals= [0], transitions= {})

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return DFA(states= 2, finals= [1], transitions= {(0, s) : 1})

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)

class CharGroupNode(AtomicNode):
    def evaluate(self):
        automatons = []
        for char in self.lex:
            automatons.append(SymbolNode(char).evaluate())
        automaton = automatons[0]
        for atm in automatons:
            automaton = automata_union(automaton, atm)
        return automaton

def get_characters_between(a, b):
    characters = []
    for i in range(ord(a), ord(b) + 1):
        characters.append(chr(i))
    return set(characters)

def get_all_characters():
    all_chars = get_characters_between('!', chr(126))
    all_chars.add(' ')
    return all_chars

all_chars = get_all_characters()

G = Grammar()

#vagamente inspirado en la gramatica del regex real
#expression
E = G.NonTerminal('E', True)
# subexpression, term, atom, char, quantifier 
S, T, A, C, D, Q = G.NonTerminals('S T A C D Q')

pipe, star, minus, caret, opar, cpar, obrckt, cbrckt, character, epsilon = G.Terminals('| * - ^ ( ) [ ] character ε')

fixed_tokens = {
        '|': Token('|', pipe),
        '*': Token('*', star),
        '-': Token('-', minus),
        '^': Token('^', caret),
        'ε': Token('ε', epsilon),
        '(': Token('(', opar),
        ')': Token(')', cpar),
        '[': Token('[', obrckt),
        ']': Token(']', cbrckt)
        }

# A expression is a subexpression or a union of subexpressions
# A subexpression is a term or a concatenation of terms
# A term is an atom, or a quantified atom
# An atom is epsilon, char, digit, letter or an expresion between parenthesis

E %= S, lambda h, s : s[1]
E %= S + pipe + E, lambda h, s : UnionNode(s[1], s[3])
S %= T, lambda h, s : s[1]
S %= T + S, lambda h, s : ConcatNode(s[1], s[2])
T %= A, lambda h, s : s[1]
T %= A + star, lambda h, s : ClosureNode(s[1])
A %= epsilon, lambda h, s : EpsilonNode(s[1])
A %= C, lambda h, s : s[1]
A %= opar + E + cpar, lambda h, s : s[2]
C %= character, lambda h, s : SymbolNode(s[1])
C %= obrckt + D, lambda h, s : CharGroupNode(s[2])
C %= obrckt + caret + D, lambda h, s : CharGroupNode(all_chars.difference(s[3]))
D %= character + D, lambda h, s : set([s[1]]).union(s[2])
D %= character + minus + character + D, lambda h, s : get_characters_between(s[1], s[3]).union(s[4])
D %= cbrckt, lambda h, s : set()