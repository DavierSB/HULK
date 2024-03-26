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
from token_types import tokens

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
    #First we remove non-scaped whitespaces that are not within a literal
    new_text = ''
    open_quote = False
    if skip_whitespaces:
        for i in range(len(text)):
            previous_char = text[i-1] if i > 0 else None
            char = text[i]
            scaped = (previous_char == '\\')
            if char == '"':
                if (not open_quote):
                    open_quote = True
                if open_quote and not scaped:
                    open_quote = False
            if char.isspace() and not scaped and not open_quote:
                continue
            new_text += text[i]
    text = new_text

    #Now we tokenize
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
    #print([token.lex for token in tokens])
    #input()
    return tokens

def literal_test():
    dfa = Regex(tokens['LITERAL']).automaton
    assert not dfa.recognize('')
    assert dfa.recognize('"a"')
    assert dfa.recognize('"Hola"')
    assert dfa.recognize('"Hola Mundo"')
    assert dfa.recognize('"Hola me llamo \\"Davier\\" que bola"')

#literal_test()
#print("LLEGUEEEEEE")