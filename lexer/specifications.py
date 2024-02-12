from automata import *
from conditions import *

def define_language():
    
    language = automata()

    for i in range(44):
        language.add_node(node())
    
    #type num
    language.add_transition(0, 1, is_digit)
    language.add_transition(1, 1, is_digit)
    language.set_output(1, 'NUM')
    language.add_transition(1, 2, is_equal_to('.'))
    language.add_transition(2, 3, is_digit)
    language.add_transition(3, 3, is_digit)
    language.set_output(3, 'NUM')
    language.add_transition(3, 4, is_any_of(['e', 'E']))
    language.add_transition(1, 4, is_any_of(['e', 'E']))
    language.add_transition(4, 5, is_equal_to('-'))
    language.add_transition(4, 6, is_digit)
    language.add_transition(5, 6, is_digit)
    language.add_transition(6, 6, is_digit)
    language.set_output(6, 'NUM')

    #type id
    language.add_transition(0, 7, is_alpha)
    language.add_transition(7, 7, is_alpha_or_digit_or__)
    language.set_output(7, 'ID')

    #type literal
    language.add_transition(0, 8, is_equal_to('"'), False)
    language.add_transition(8, 8, is_none_of(['\\', '"']))
    language.add_transition(9, 8, is_anything)
    language.add_transition(8, 9, is_equal_to('\\'), False)
    language.add_transition(8, 10, is_equal_to('"'), False)
    language.set_output(10, 'LITERAL')

    #type ignore
    language.add_transition(0, 0, is_any_of([' ', '\n', '\t']), False)
    language.add_transition(0, 12, is_equal_to('\\'), False)
    language.add_transition(12, 13, is_equal_to('\\'), False)
    language.add_transition(13, 13, is_not('\n'), False)
    language.add_transition(13, 14, is_equal_to('\n'), False)
    language.set_output(14, 'IGNORE')

    #type separator
    language.add_transition(0, 15, is_equal_to('('))
    language.set_output(15, 'LPAREN')
    language.add_transition(0, 16, is_equal_to(')'))
    language.set_output(16, 'RPAREN')
    language.add_transition(0, 17, is_equal_to('['))
    language.set_output(17, 'LBRACKET')
    language.add_transition(0, 18, is_equal_to(']'))
    language.set_output(18, 'RBRACKET')
    language.add_transition(0, 19, is_equal_to('{'))
    language.set_output(19, 'LBRACE')
    language.add_transition(0, 20, is_equal_to('}'))
    language.set_output(20, 'RBRACE')
    language.add_transition(0, 26, is_equal_to(';'))
    language.set_output(26, 'SEMICOLON')
    language.add_transition(0, 27, is_equal_to(':'))
    language.set_output(27, 'COLON')
    language.add_transition(0, 36, is_equal_to(','))
    language.set_output(36, 'COMMA')
    language.add_transition(0, 39, is_equal_to('.'))
    language.set_output(39, 'DOT')

    #type operator
    language.add_transition(0, 21, is_equal_to('+'))
    language.set_output(21, 'PLUS')
    language.add_transition(0, 22, is_equal_to('-'))
    language.set_output(22, 'MINUS')
    language.add_transition(0, 23, is_equal_to('*'))
    language.set_output(23, 'POWER')
    language.add_transition(0, 24, is_equal_to('\\'))
    language.set_output(24, 'DIVIDE')
    language.add_transition(23, 25, is_equal_to('*'))
    language.add_transition(0, 25, is_equal_to('^'))
    language.set_output(25, 'POWER')
    language.add_transition(0, 35, is_equal_to('@'))
    language.set_output(35, 'CONCAT')
    language.add_transition(35, 42, is_equal_to('@'))
    language.set_output(42, 'CONCAT')
    language.add_transition(0, 38, is_equal_to('%'))
    language.set_output(38, 'MODULE')
    language.add_transition(0, 40, is_equal_to('|'))
    language.set_output(40, 'OR')
    language.add_transition(0, 41, is_equal_to('&'))
    language.set_output(41, 'AND')

    #type assign
    language.add_transition(0, 29, is_equal_to('='))
    language.set_output(29, 'ASSIGN')
    language.add_transition(27, 28, is_equal_to('='))
    language.set_output(28, 'REASSIGN')
    language.add_transition(29, 37, is_equal_to('>'))
    language.set_output(37, 'LAMBDA')

    #type comparator
    language.add_transition(29, 30, is_equal_to('='))
    language.set_output(30, 'COMPARER')
    language.add_transition(0, 31, is_equal_to('<'))
    language.set_output(31, 'COMPARER')
    language.add_transition(31, 32, is_equal_to('='))
    language.set_output(32, 'COMPARER')
    language.add_transition(0, 33, is_equal_to('>'))
    language.set_output(33, 'COMPARER')
    language.add_transition(33, 34, is_equal_to('='))
    language.set_output(34, 'COMPARER')
    
    reserved_words = {
        'true' : 'TRUE',                                 
        'false' : 'FALSE',
        'PI' : 'CONSTANT',
        'e' : 'CONSTANT',
        'print' : 'PRINT',
        'sqrt' : 'SQRT',
        'sin' : 'SIN',
        'cos' : 'COS',
        'exp' : 'EXP',
        'log' : 'LOG',
        'rand' : 'RAND',
        'function' : 'FUNCTION',
        'let' : 'LET',
        'in' : 'IN',
        'if' : 'IF',
        'else' : 'ELSE',
        'while' : 'WHILE',
        'for' : 'FOR',
        'range' : 'RANGE',
        'type' : 'TYPE',
        'self' : 'SELF',
        'new' : 'NEW',
        'inherits' : 'INHERITS',
        'protocol' : 'PROTOCOL',
        'extends' : 'EXTENDS'
    }

    return language, reserved_words
