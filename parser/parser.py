from stack import Stack
from queue import Queue
from typing import List, Dict, Set
from cmp.pycompiler import Grammar, Production, Symbol, Sentence
from grammars import Grammar_LR, Grammar_LL
from utils import subSentence
import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir)


def apply_production(sentence : Sentence, symbol_idx : int, production : Production) -> Sentence:
    return subSentence(sentence, 0, symbol_idx) + production.Right + subSentence(sentence, symbol_idx + 1)

def parse_LR(code : List[Symbol], grammar : Grammar_LR) -> List[Production]:
    actions, goto = grammar.get_table()
    stack = Stack()
    stack.push(0)
    idx = 0
    productions = []
    while True:
        state = stack.peek()
        symbol = code[idx]
        current_action = actions[(state, symbol)]
        if current_action.is_shift():
            stack.push(current_action.next_state)
            idx = idx + 1
            continue
        if current_action.is_reduce():
            current_production = current_action.production
            productions.append(current_production)
            for _ in range(len(current_production.Right)):
                stack.pop()
            stack.push(goto[stack.peek()][current_production.Left])
            continue
        if current_action.is_error():
            pass
        if current_action.is_accept():
            break
    return productions

# Aun no manejamos errores
def parse_LL(code : List[Symbol], grammar : Grammar_LL):
    table = grammar.get_table()
    sentence = grammar.startSymbol + grammar.Epsilon
    productions = []
    idx_for_reading_code = 0
    idx_within_current_sentence = 0
    while idx_within_current_sentence < len(sentence):
        token = grammar.Epsilon
        if idx_for_reading_code < len(code):
            token = code[idx_for_reading_code]
        symbol = sentence[idx_within_current_sentence]
        production = table[symbol, token]
        if (symbol.IsNonTerminal) and (production is None):
            print("El codigo tiene errores")
            break
        sentence = apply_production(sentence, idx_within_current_sentence, production)
        productions.append(production)
        while (idx_within_current_sentence < len(sentence)) and (sentence[idx_within_current_sentence].IsTerminal):
            if sentence[idx_within_current_sentence] != code[idx_for_reading_code]:
                print("Se esperaba un " + str(sentence[idx_within_current_sentence]) + " pero se encontro un " + str(code[idx_for_reading_code]))
                break
            idx_for_reading_code = idx_for_reading_code + 1
            idx_within_current_sentence = idx_within_current_sentence + 1
    return productions