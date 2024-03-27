import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.pycompiler import Grammar
G = Grammar()

#Non Terminals
init_ = G.NonTerminal('INIT', True)
program = G.NonTerminal('PROGRAM')
statement, expression = G.NonTerminals('STAMENT EXPRESSION')
arithmetic_expression = G.NonTerminal('ARITHMETIC_EXPRESSION')
factor, power_term, arithmetic_term = G.NonTerminals('FACTOR POWER_TERM ARITHMETIC_TERM')
sum_operator, mult_operator = G.NonTerminals('SUM_OPERATOR MULT_OPERATOR')

#Terminales
number, boolean, literal, id = G.Terminals('NUMBER BOOLEAN LITERAL ID')
plus, minus, times, divide, module, power, concat = G.Terminals('PLUS MINUS TIMES DIVIDE MODULE POWER CONCAT')
comparer = G.Terminals('COMPARER')
and_, or_, not_ = G.Terminals('AND OR NOT')
dot, colon, comma, semicolon = G.Terminals('DOT COLON COMMA SEMICOLON')
lparen, rparen, lbrace, rbrace = G.Terminals('LPAREN RPAREN LBRACE RBRACE')
lambda_, assign, reassign = G.Terminals('LAMBDA ASSIGN REASSIGN')
math_function, print, constant = G.Terminals('MATH_FUNCTION PRINT CONSTANT')
let_, in_, function_ = G.Terminals('LET IN FUNCTION')
if_, else_, while_, for_, range_ = G.Terminals('IF ELSE WHILE FOR RANGE')
type_, self_, new_ = G.Terminals('TYPE SELF NEW')
inherits, protocol, extends = G.Terminals('INHERITS PROTOCOL EXTENDS')

init_ %= program

program %= statement + program
program %= expression + semicolon

expression %= arithmetic_expression
expression %= id

arithmetic_expression %= factor + sum_operator + arithmetic_expression
arithmetic_expression %= factor

factor %= power_term + mult_operator + factor
factor %= power_term

power_term %= arithmetic_term
power_term %= arithmetic_term + power + power_term

arithmetic_term %= number
arithmetic_term %= lparen + expression + rparen

sum_operator %= plus
sum_operator %= minus

mult_operator %= times
mult_operator %= divide
mult_operator %= module