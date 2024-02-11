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
    language.add_transition(1, 2, is_equal_to('.'), True)
    language.add_transition(2, 3, is_digit, True)
    language.add_transition(3, 3, is_digit, True)
    language.set_output(3, 'num')
    language.add_transition(3, 4, is_equal_to('e'), True)
    language.add_transition(1, 4, is_equal_to('e'), True)
    language.add_transition(4, 5, is_equal_to('-'), True)
    language.add_transition(4, 6, is_digit, True)
    language.add_transition(5, 6, is_digit, True)
    language.add_transition(6, 6, is_digit, True)
    language.set_output(6, 'num')

    #type id
    language.add_transition(0, 7, is_alpha, True)
    language.add_transition(7, 7, is_alpha_or_digit_or__, True)
    language.set_output(7, 'id')

    #type literal
    language.add_transition(0, 8, is_equal_to('"'), False)
    language.add_transition(8, 8, is_none_of(['\\', '"']), True)
    language.add_transition(9, 8, is_anything, True)
    language.add_transition(8, 9, is_equal_to('\\'), False)
    language.add_transition(8, 10, is_equal_to('"'), False)
    language.set_output(10, 'literal')

    #type ignore
    language.add_transition(0, 0, is_any_of([' ', '\n', '\t']), False)
    language.add_transition(0, 12, is_equal_to('\\'), False)
    language.add_transition(12, 13, is_equal_to('\\'), False)
    language.add_transition(13, 13, is_not('\n'), False)
    language.add_transition(13, 14, is_equal_to('\n'), False)
    language.set_output(14, 'ignore')

    #type separator
    language.add_transition(0, 15, is_equal_to('('), True)
    language.set_output(15, 'opened_parent')
    language.add_transition(0, 16, is_equal_to(')'), True)
    language.set_output(16, 'closed_parent')
    language.add_transition(0, 17, is_equal_to('['), True)
    language.set_output(17, 'opened_bracket')
    language.add_transition(0, 18, is_equal_to(']'), True)
    language.set_output(18, 'closed_bracket')
    language.add_transition(0, 19, is_equal_to('{'), True)
    language.set_output(19, 'opened_brace')
    language.add_transition(0, 20, is_equal_to('}'), True)
    language.set_output(20, 'closed_brace')
    language.add_transition(0, 26, is_equal_to(';'), True)
    language.set_output(26, 'semicolon')
    language.add_transition(0, 27, is_equal_to(':'), True)
    language.set_output(27, 'colon')
    language.add_transition(0, 36, is_equal_to(','), True)
    language.set_output(36, 'comma')
    language.add_transition(0, 39, is_equal_to('.'), True)
    language.set_output(39, 'dot')

    #type operator
    language.add_transition(0, 21, is_equal_to('+'), True)
    language.set_output(21, 'plus')
    language.add_transition(0, 22, is_equal_to('-'), True)
    language.set_output(22, 'minus')
    language.add_transition(0, 23, is_equal_to('*'), True)
    language.set_output(23, 'asterisk')
    language.add_transition(0, 24, is_equal_to('\\'), True)
    language.set_output(24, 'slash')
    language.add_transition(0, 25, is_equal_to('^'), True)
    language.set_output(25, 'caret')
    language.add_transition(0, 35, is_equal_to('@'), True)
    language.set_output(35, 'concat')
    language.add_transition(35, 42, is_equal_to('@'), True)
    language.set_output(42, 'concat')
    language.add_transition(0, 38, is_equal_to('%'), True)
    language.set_output(38, 'modulo')
    language.add_transition(0, 40, is_equal_to('|'), True)
    language.set_output(40, 'pipe')
    language.add_transition(0, 41, is_equal_to('&'), True)
    language.set_output(41, 'ampersand')

    #type assign
    language.add_transition(0, 29, is_equal_to('='), True)
    language.set_output(29, 'assign')
    language.add_transition(27, 28, is_equal_to(':='), True)
    language.set_output(28, 'reassign')
    language.add_transition(29, 37, is_equal_to('>'), True)
    language.set_output(37, 'lambda')

    #type comparator
    language.add_transition(29, 30, is_equal_to('='), True)
    language.set_output(30, 'comparer')
    language.add_transition(0, 31, is_equal_to('<'), True)
    language.set_output(31, 'comparer')
    language.add_transition(31, 32, is_equal_to('='), True)
    language.set_output(32, 'comparer')
    language.add_transition(0, 33, is_equal_to('>'), True)
    language.set_output(33, 'comparer')
    language.add_transition(33, 34, is_equal_to('='), True)
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
