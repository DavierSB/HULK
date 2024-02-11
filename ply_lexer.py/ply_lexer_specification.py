import ply.lex as lex
import re

reserved_words = {
    'true' : 'TRUE',                                 
    'false' : 'FALSE',
    'PI' : 'CONSTANT',
    'E' : 'CONSTANT',
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

operator_tokens = {
    'PLUS' : r'\+',
    'MINUS' : r'-',
    'TIMES' : r'\*',
    'DIVIDE': r'/',
    'MODULE' : r'\%',
    'POWER' : r'\*\*|\^',
    'CONCAT' : r'@|@@',
    'LAMBDA' : r'=\>',
    'ASSIGN' : r'=',
    'REASSIGN' : r':=',
    'COMPARER' : r'< | \> | <= | \>= | == | !=',
    'AND' : r'&',
    'OR' : r'\|',
    'NOT' : r'!',
    'DOT' : r'\.',
    'COLON' : r':',
    'ESCAPE' : r'\\'
}

punctuation_tokens = {
    'COMMA' : r',',
    'SEMICOLON' : r';',
    'LPAREN' : r'\(',
    'RPAREN' : r'\)',
    'LBRACE' : r'\{',
    'RBRACE' : r'\}',
    'QUOTE' : r'"'
}

special_treated_tokens = [
   'ID',
   'NUMBER',
   'STRING'
]

tokens = list(operator_tokens.keys()) + list(punctuation_tokens.keys())

for token in tokens:
    if token in operator_tokens:
        globals()['t_' + token] = operator_tokens[token]
    else:
        globals()['t_' + token] = punctuation_tokens[token]

tokens = tokens + list(reserved_words.values()) + special_treated_tokens

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_words.get(t.value,'ID')
    return t

def t_STRING(t):
    r'"(?:[^"\\]|\\.)*"'
    return t

def t_NUMBER(t):
    r'-?(0|[1-9][0-9]*)(\.[0-9]+)?'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)