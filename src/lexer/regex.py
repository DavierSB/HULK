import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/automata')
sys.path.insert(0, current_dir + '/src/parser')
from regex_grammar import G, fixed_tokens, character
from automata.automata_utils import nfa_to_dfa
from parser.slr1_parser import SLR1Parser
from cmp.utils import Token
from cmp.evaluation import evaluate_reverse_parse
from parser.slr1_parser import SLR1Parser

class Regex:
    def __init__(self, pattern : str):
        tokens = regex_tokenizer(pattern)
        filtered_tokens = [token.token_type for token in tokens]
        parser = SLR1Parser(G)
        right_parse, operations = parser(filtered_tokens, get_shift_reduce= True)
        ast = evaluate_reverse_parse(right_parse, operations, tokens)
        nfa = ast.evaluate()
        dfa = nfa_to_dfa(nfa)
        self.automaton = dfa

def regex_tokenizer(text : str, skip_whitespaces=True):
    if skip_whitespaces:
        text = text.replace(' ', '')
    tokens = []
    scaped = False
    for i in range(len(text)):
        previous_char = text[i-1] if i > 0 else None
        char = text[i]
        next_char = text[i+1] if i + 1 < len(text) else None
        if (not scaped) and (char == '\\'):
            scaped = True
            continue
        if (not scaped) and (char in fixed_tokens):
            tokens.append(fixed_tokens[char])
        else:
            tokens.append(Token(char, character))
            scaped = False
        
    tokens.append(Token('$', G.EOF))
    return tokens

def basic_test():
    dfa = Regex('a*(a|b)*cd | ε').automaton
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

def scapes_test():
    def put_scapes(pattern):
        new_pattern = pattern.replace('K', '\\')
        return new_pattern
    dfa = Regex(put_scapes('(K*K*KK*)*')).automaton
    assert dfa.recognize('')
    assert dfa.recognize('**')
    assert dfa.recognize('****')
    assert dfa.recognize('********')
    assert dfa.recognize('**\\\\\\')
    assert dfa.recognize(put_scapes('**KKKKKK'))

    assert not dfa.recognize('***')
    assert not dfa.recognize('*****')
    assert not dfa.recognize('*******')

#basic_test()
scapes_test()
#print("LLEGUEEEEEEEEE")