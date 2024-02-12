from automata import *
from conditions import *
import specificator

def define_language():
    
    language = Automata()

    for i in range(1, 44):
        language.add_node(Node(i))
    
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

    specificator.add_tokens(language, load_tokens())
    
    return language, reserved_words()



def load_tokens():
    operator_tokens = {
        '+' : 'PLUS',
        '-' : 'MINUS',
        '*' : 'TIMES',
        '/' : 'DIVIDE',
        '%' : 'MODULE',
        '^' : 'POWER',
        '**' : 'POWER',
        '@' : 'CONCAT',
        '@@' : 'CONCAT',
        '=>' : 'LAMBDA',
        '=' : 'ASSIGN',
        ':=' : 'REASSIGN',
        '<' : 'COMPARER',
        '>' : 'COMPARER',
        '<=' : 'COMPARER',
        '>=' : 'COMPARER',
        '==' : 'COMPARER',
        '!=' : 'COMPARER',
        '&' : 'AND',
        '|' : 'OR',
        '!' : 'NOT',
        '.' : 'DOT',
        ':' : 'COLON',
        '\\' : 'ESCAPE'
    }

    punctuation_tokens = {
        ',' : 'COMMA',
        ';' : 'SEMICOLON',
        '(' : 'LPAREN',
        ')' : 'RPAREN',
        '{' : 'LBRACE',
        '}' : 'RBRACE',
        '"' : 'QUOTE'
    }
    operator_tokens.update(punctuation_tokens)
    return operator_tokens

def reserved_words():
    return {
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