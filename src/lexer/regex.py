import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/automata')
sys.path.insert(0, current_dir + '/src/parser')
from automata.nfa import NFA
from automata.dfa import DFA
from automata.automata_utils import nfa_to_dfa, automata_closure, automata_concatenation, automata_union
from parser.slr1_parser import SLR1Parser
from cmp.ast import AtomicNode, UnaryNode, BinaryNode
from cmp.pycompiler import Grammar
from cmp.utils import Token
from cmp.evaluation import evaluate_reverse_parse
from parser.slr1_parser import SLR1Parser
from IPython.display import display

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
        lvalue, rvalue = self.lex
        automaton = SymbolNode(lvalue).evaluate()
        for idx in range(ord(lvalue) + 1, ord(rvalue) + 1):
            automaton = automata_union(automaton, SymbolNode(chr(idx)).evaluate())
        return automaton


G = Grammar()

#vagamente inspirado en la gramatica del regex real
#expression
E = G.NonTerminal('E', True)
# subexpression, term, atom, char, quantifier 
S, T, A, C, Q = G.NonTerminals('S T A C Q')

pipe, star, minus, opar, cpar, obrckt, cbrckt, character, epsilon = G.Terminals('| * - ( ) [ ] character ε')

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
C %= obrckt + character + minus + character + cbrckt, lambda h, s : CharGroupNode((s[2], s[4]))

def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    fixed_tokens = {
        '|': Token('|', pipe),
        '*': Token('*', star),
        '-': Token('-', minus),
        'ε': Token('ε', epsilon),
        '(': Token('(', opar),
        ')': Token(')', cpar),
        '[': Token('[', obrckt),
        ']': Token(']', cbrckt)
        }
    # Your code here!!!
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        if char in fixed_tokens:
            tokens.append(fixed_tokens[char])
        else:
            tokens.append(Token(char, character))
        
    tokens.append(Token('$', G.EOF))
    return tokens

tokens = regex_tokenizer('a*(a|b)*cd | ε',G)
filtered_tokens = [token.token_type for token in tokens]

parser = SLR1Parser(G)
right_parse, operations = parser(filtered_tokens, get_shift_reduce= True)

ast = evaluate_reverse_parse(right_parse, operations, tokens)
nfa = ast.evaluate()
dfa = nfa_to_dfa(nfa)

def standard_test(dfa):
    assert dfa.recognize('')
    assert dfa.recognize('cd')
    assert dfa.recognize('aaaaacd')
    assert dfa.recognize('bbbbbcd')
    assert dfa.recognize('bbabababcd')
    assert dfa.recognize('aaabbabababcd')
    
    assert not dfa.recognize('cda')
    assert not dfa.recognize('aaaaa')
    assert not dfa.recognize('bbbbb')
    assert not dfa.recognize('ababba')
    assert not dfa.recognize('cdbaba')
    assert not dfa.recognize('cababad')
    assert not dfa.recognize('bababacc')

def groups_test(dfa):
    assert dfa.recognize('7.25')

groups_test(dfa)