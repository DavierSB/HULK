from nfa import NFA
from typing import List, Dict, Tuple

class DFA(NFA):
    
    def __init__(self, states : int, finals : List[int], transitions : Dict[Tuple[int, str], int], start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol : str) -> None:
        self.current = self.transitions[self.current].get(symbol, [None])[0]
    
    def _reset(self) -> None:
        self.current = self.start
        
    def recognize(self, string : str) -> bool:
        for s in string:
            self._move(s)
            if self.current == None:
                self._reset()
                return False
        recognized = (self.current in self.finals)
        self._reset()
        return recognized