line_jump = chr(10)

tokens = {
    'NUMBER' : '(0|[1-9][0-9]*) | (0|[1-9][0-9]*).([0-9][0-9]*)',
    'ID' : '([a-zA-Z_])([a-zA-Z0-9_])*',
    'LITERAL' : '"([^\\\\"]*(\\\\[^])*)*"',
    'PLUS' : '+',
    'MINUS' : '\-',
    'TIMES' : '\*',
    'DIVIDE' : '/',
    'MODULE' : '%',
    'POWER' : '\^|\*\*',
    'CONCAT' : '@@*',
    'LAMBDA' : '=>',
    'ASSIGN' : '=',
    'REASSIGN' : ':=',
    'COMPARER' : '<|>|<=|>=|==|!=',
    'AND' : '&',
    'OR' : '\|',
    'NOT' : '!',
    'DOT' : '.',
    'COLON' : ':',
    'COMMA' : ',',
    'SEMICOLON' : ';',
    'LPAREN' : '\(',
    'RPAREN' : '\)',
    'LBRACE' : '\{',
    'RBRACE' : '\}',
    'QUOTE' : '"',
    'IGNORE' : '(\ |' + line_jump + ')(\ |' + line_jump + ')*'
    }

reserved_words = {
        'BOOLEAN' : 'true|false',
        'CONSTANT' : 'PI|E', #pie jj
        'MATH_FUNCTION' : 'sqrt|sin|cos|exp|log|rand',
        'PRINT' : 'print',
        'FUNCTION' : 'function',
        'LET' : 'let',
        'IN' : 'in',
        'IF' : 'if',
        'ELSE' : 'else',
        'WHILE' : 'while',
        'FOR' : 'for',
        'RANGE' : 'range',
        'TYPE' : 'type',
        'SELF' : 'self',
        'NEW' : 'new',
        'INHERITS' : 'inherits',
        'PROTOCOL' : 'protocol',
        'EXTENDS' : 'extends'
    }