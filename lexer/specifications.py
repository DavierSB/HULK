from automata import *
from conditions import *

def define_language():
    
    language = automata()

    for i in range(42):
        language.add_node(node())
    
    #type num
    language.add_transition(0, 1, is_digit, True)
    language.add_transition(1, 1, is_digit, True)
    language.set_output(1, 'num')
    language.add_transition(1, 2, is_dot, True)
    language.add_transition(2, 3, is_digit, True)
    language.add_transition(3, 3, is_digit, True)
    language.set_output(3, 'num')
    language.add_transition(3, 4, is_e, True)
    language.add_transition(1, 4, is_e, True)
    language.add_transition(4, 5, is_minus, True)
    language.add_transition(4, 6, is_digit, True)
    language.add_transition(5, 6, is_digit, True)
    language.add_transition(6, 6, is_digit, True)
    language.set_output(6, 'num')

    #type id
    language.add_transition(0, 7, is_alpha, True)
    language.add_transition(7, 7, is_alpha_or_digit_or__, True)
    language.set_output(7, 'id')

    #type literal
    language.add_transition(0, 8, is_quote, False)
    language.add_transition(8, 8, is_not_backslash_or_quote, True)
    language.add_transition(9, 8, is_everything, True)
    language.add_transition(8, 9, is_backslash, False)
    language.add_transition(8, 10, is_quote, False)
    language.set_output(10, 'literal')

    #type ignore
    language.add_transition(0, 0, is_ignore, False)
    language.add_transition(0, 12, is_backslash, False)
    language.add_transition(12, 13, is_backslash, False)
    language.add_transition(13, 13, is_not_newline, False)
    language.add_transition(13, 14, is_newline, False)
    language.set_output(14, 'ignore')

    #type separator
    language.add_transition(0, 15, is_opened_parenthesis, True)
    language.set_output(15, 'opened_parent')
    language.add_transition(0, 16, is_closed_parenthesis, True)
    language.set_output(16, 'closed_parent')
    language.add_transition(0, 17, is_opened_bracket, True)
    language.set_output(17, 'opened_bracket')
    language.add_transition(0, 18, is_closed_bracket, True)
    language.set_output(18, 'closed_bracket')
    language.add_transition(0, 19, is_opened_brace, True)
    language.set_output(19, 'opened_brace')
    language.add_transition(0, 20, is_closed_brace, True)
    language.set_output(20, 'closed_brace')
    language.add_transition(0, 26, is_semicolon, True)
    language.set_output(26, 'semicolon')
    language.add_transition(0, 27, is_colon, True)
    language.set_output(27, 'colon')
    language.add_transition(0, 36, is_comma, True)
    language.set_output(36, 'comma')
    language.add_transition(0, 39, is_dot, True)
    language.set_output(39, 'dot')

    #type operator
    language.add_transition(0, 21, is_plus, True)
    language.set_output(21, 'plus')
    language.add_transition(0, 22, is_minus, True)
    language.set_output(22, 'minus')
    language.add_transition(0, 23, is_asterisk, True)
    language.set_output(23, 'asterisk')
    language.add_transition(0, 24, is_slash, True)
    language.set_output(24, 'slash')
    language.add_transition(0, 25, is_caret, True)
    language.set_output(25, 'caret')
    language.add_transition(0, 35, is_arroba, True)
    language.set_output(35, 'concat')
    language.add_transition(35, 42, is_arroba, True)
    language.set_output(42, 'concat')
    language.add_transition(0, 38, is_mod, True)
    language.set_output(38, 'modulo')
    language.add_transition(0, 40, is_pipe, True)
    language.set_output(40, 'pipe')
    language.add_transition(0, 41, is_ampersand, True)
    language.set_output(41, 'ampersand')

    #type assign
    language.add_transition(0, 29, is_equal, True)
    language.set_output(29, 'assign')
    language.add_transition(27, 28, is_equal, True)
    language.set_output(28, 'reassign')
    language.add_transition(29, 37, is_greater_than, True)
    language.set_output(37, 'lambda')

    #type comparator
    language.add_transition(29, 30, is_equal, True)
    language.set_output(30, 'comparer')
    language.add_transition(0, 31, is_less_than, True)
    language.set_output(31, 'comparer')
    language.add_transition(31, 32, is_equal, True)
    language.set_output(32, 'comparer')
    language.add_transition(0, 33, is_greater_than, True)
    language.set_output(33, 'comparer')
    language.add_transition(33, 34, is_equal, True)
    language.set_output(34, 'comparer')
    
    reserved_words = {
        'true' : 'true',
        'false' : 'false',
        'PI' : 'constant',
        'E' : 'constant',
        'print' : 'print',
        'sqrt' : 'sqrt',
        'sqrt' : 'sqrt',
        'cos' : 'cos',
        'exp' : 'exp',
        'log' : 'log',
        'rand' : 'rand',
        'function' : 'function',
        'let' : 'let',
        'in' : 'in',
        'if' : 'if',
        'else' : 'else',
        'while' : 'while',
        'for' : 'for',
        'range' : 'range',
        'type' : 'type',
        'self' : 'self',
        'new' : 'new',
        'inherits' : 'inherits',
        'protocol' : 'protocol',
        'extends' : 'extends'
    }

    return language, reserved_words
