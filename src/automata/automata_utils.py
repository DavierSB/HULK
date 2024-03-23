from nfa import NFA
from dfa import DFA
from typing import List
import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.utils import ContainerSet


def move(automaton : NFA|DFA, states : List[int], symbol : str):
    moves = set()
    for state in states:
        new_state = automaton.transitions[state].get(symbol, [None])
        if new_state[0] is not None:
            moves.update(set(new_state))
    return moves


def epsilon_closure(automaton : NFA, states : List[int]) -> ContainerSet:
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        for new_state in automaton.transitions[state].get('', []):
            if not new_state in closure:
                closure.add(new_state)
                pending.append(new_state)
                
    return ContainerSet(*closure)


def nfa_to_dfa(automaton : NFA) -> DFA:
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            next_state = move(automaton, state, symbol)
            if len(next_state) == 0:
                continue
            next_state = epsilon_closure(automaton, next_state)
            if next_state in states:
                next_state = states[states.index(next_state)]
            else:
                next_state.id = len(states)
                next_state.is_final = any(s in automaton.finals for s in next_state)
                states.append(next_state)
                pending.append(next_state)

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol] = next_state.id
    
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa


def automata_union(a1 : NFA, a2 : NFA) -> NFA:
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[d1 + origin, symbol] = [d1 + dest for dest in destinations]

    for (origin, symbol), destinations in a2.map.items():
        transitions[d2 + origin, symbol] = [d2 + dest for dest in destinations]
    
    transitions[0, ''] = [1, d2]
    
    for fs in a1.finals:
        key = (fs + d1, '')
        if not key in transitions:
            transitions[key] = []
        transitions[key].append(final)

    for fs in a2.finals:
        key = (fs + d2, '')
        if not key in transitions:
            transitions[key] = []
        transitions[key].append(final)
            
    states = a1.states + a2.states + 2
    finals = { final }
    
    
    return NFA(states, finals, transitions, start)


def automata_concatenation(a1 : NFA, a2 : NFA) -> NFA:
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[d1 + origin, symbol] = [d1 + dest for dest in destinations]
    
    for fs in a1.finals:
        key = (fs + d1, '')
        if not key in transitions:
            transitions[key] = []
        transitions[key].append(d2)

    for (origin, symbol), destinations in a2.map.items():
        transitions[d2 + origin, symbol] = [d2 + dest for dest in destinations]
    
    for fs in a2.finals:
        key = (fs + d2, '')
        if not key in transitions:
            transitions[key] = []
        transitions[key].append(final)
            
    states = a1.states + a2.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[d1 + origin, symbol] = [d1 + dest for dest in destinations]
    
    transitions[0, ''] = [1, final]
    
    for fs in a1.finals:
        key = (fs + d1, '')
        if not key in transitions:
            transitions[key] = []
        transitions[key].extend([start, final])
            
    states = a1.states +  2
    finals = { final }
    
    return NFA(states, finals, transitions, start)