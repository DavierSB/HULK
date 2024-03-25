import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/lexer')
from cmp.automata import State
from cmp.utils import Token
from lexer.regex import Regex

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            automaton, states = State.from_nfa(Regex(regex).automaton, True)
            for state in states:
                if state.final:
                    state.tag = (n, token_type)
                regexs.append(automaton)
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton)
        return start.to_deterministic()    
        
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''
        
        for symbol in string:
            if state.has_transition(symbol):
                state = state.transitions[symbol][0]
                lex = lex + symbol
                if state.final:
                    final = state if state.final else None
                    final_lex = lex
                continue
            break
                
        return final, final_lex
    
    def _tokenize(self, text):
        current_text = text
        while len(current_text):
            state, lex = self._walk(current_text)
            if state is not None:
                current_text = current_text[len(lex):]
                tags = [s.tag for s in state.state if s.tag is not None]
                _, token_type = min(tags, key= lambda x : x[0])
                yield lex, token_type
            else:
                yield current_text[0], "ERROR"
                current_text = current_text[1:]
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]