from automata import Automata, Node, Transition
from conditions import is_equal_to

def add_tokens(language : Automata, tokens):
    for token_lexeme in tokens.keys():
        add_single_token(language, token_lexeme, tokens[token_lexeme])

def add_single_token(language : Automata, token_lexeme : str, token_name : str):
    act = language.start_node
    for c in token_lexeme:
        trans = search_transition_for(act, c)
        if trans:
            act = trans.dest_node
        else:
            old_idx = act.idx
            act = create_node(language, act, c)
            language.add_transition(old_idx, act.idx, is_equal_to(c))
    language.set_output(act.idx, token_name)

def search_transition_for(act : Node, c) -> Transition:
    for trans in act.transitions:
        if trans.condition(c):
            return trans
    return None

def create_node(language : Automata, act : Node, c) -> Node:
    idx = len(language.nodes) - 1
    node = Node(idx)
    language.add_node(node)
    language.add_transition(act.idx, idx, is_equal_to(c))
    return node