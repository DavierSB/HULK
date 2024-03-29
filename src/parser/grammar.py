import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.pycompiler import Grammar
G = Grammar()

#NonTerminals
program = G.NonTerminal('PROGRAM', True)
expression, statement = G.NonTerminals('EXPRESSION STATEMENT')
disjunction, conjunction, proposition, boolean_term, concatenation, arithmetic_expression, sum_operator, factor, mult_operator, power_term, monomial, term = G.NonTerminals('DISJUNCTION CONJUNCTION PROPOSITION BOOLEAN_TERM CONCATENATION ARITHMETIC_EXPRESSION SUM_OPERATOR FACTOR MULT_OPERATOR POWER_TERM MONOMIAL TERM')
function_call, function_name, arguments = G.NonTerminals('FUNCTION_CALL FUNCTION_NAME ARGUMENTS')
let_expression, declarations, type_annotation, type_name = G.NonTerminals('LET_EXPRESSION DECLARATIONS TYPE_ANNOTATION TYPE_NAME')
if_expression, if_body = G.NonTerminals('IF_EXPRESSION IF_BODY')
while_expression, for_expression, instantiation = G.NonTerminals('WHILE_EXPRESSION FOR_EXPRESSION INSTANTIATION')
expression_block, expression_list = G.NonTerminals('EXPRESSION_BLOCK EXPRESSION_LIST')
standalone_expression = G.NonTerminal('STANDALONE_EXPRESSION')

#Terminales
number, boolean, literal, id = G.Terminals('NUMBER BOOLEAN LITERAL ID')
plus, minus, times, divide, module, power, concat = G.Terminals('PLUS MINUS TIMES DIVIDE MODULE POWER CONCAT')
comparer = G.Terminal('COMPARER')
and_, or_, not_ = G.Terminals('AND OR NOT')
dot, colon, comma, semicolon = G.Terminals('DOT COLON COMMA SEMICOLON')
lparen, rparen, lbrace, rbrace = G.Terminals('LPAREN RPAREN LBRACE RBRACE')
lambda_, assign, reassign = G.Terminals('LAMBDA ASSIGN REASSIGN')
math_function, print_, constant = G.Terminals('MATH_FUNCTION PRINT CONSTANT')
let_, in_, function_ = G.Terminals('LET IN FUNCTION')
if_, else_, elif_, while_, for_, range_ = G.Terminals('IF ELSE ELIF WHILE FOR RANGE')
type_, self_, new_ = G.Terminals('TYPE SELF NEW')
inherits, protocol, extends = G.Terminals('INHERITS PROTOCOL EXTENDS')
predefined_type = G.Terminal('PREDEFINED_TYPE')

program %= expression + semicolon
program %= standalone_expression
program %= statement + program

standalone_expression %= let_ + declarations + in_ + standalone_expression
standalone_expression %= if_ + if_body + else_ + standalone_expression
standalone_expression %= while_ + lparen + expression + rparen + standalone_expression
standalone_expression %= for_ + lparen + id + type_annotation + in_ + expression + rparen + standalone_expression
standalone_expression %= expression_block

expression %= disjunction
expression %= let_expression
expression %= if_expression
expression %= while_expression
expression %= for_expression
expression %= instantiation
expression %= id + reassign + expression
expression %= expression_block

disjunction %= conjunction
disjunction %= conjunction + or_ + disjunction

conjunction %= proposition
conjunction %= proposition + and_ + conjunction

proposition %= boolean_term
proposition %= not_ + proposition

boolean_term %= concatenation
boolean_term %= concatenation + comparer + boolean_term

concatenation %= arithmetic_expression
concatenation %= arithmetic_expression + concat + concatenation

arithmetic_expression %= factor
arithmetic_expression %= factor + sum_operator + arithmetic_expression

sum_operator %= plus
sum_operator %= minus

factor %= power_term
factor %= power_term + mult_operator + factor

mult_operator %= times
mult_operator %= divide
mult_operator %= module

power_term %= monomial
power_term %= monomial + power + power_term

monomial %= term
monomial %= minus + term

term %= number
term %= literal
term %= boolean
term %= id
term %= constant
term %= function_call
term %= self_
term %= term + dot + id
term %= term + dot + function_call
term %= lparen + arithmetic_expression + rparen

function_call %= function_name + lparen + arguments + rparen

function_name %= id
function_name %= math_function
function_name %= print_
function_name %= range_

arguments %= expression + comma + arguments
arguments %= expression
arguments %= G.Epsilon

let_expression %= let_ + declarations + in_ + expression

declarations %= id + type_annotation + assign + expression
declarations %= id + type_annotation + assign + expression + comma + declarations

type_annotation %= colon + type_name
type_annotation %= G.Epsilon

type_name %= id
type_name %= predefined_type

if_expression %= if_ + if_body + else_ + expression

if_body %= lparen + expression + rparen + expression
if_body %= lparen + expression + rparen + expression + elif_ + if_body

while_expression %= while_ + lparen + expression + rparen + expression

for_expression %= for_ + lparen + id + type_annotation + in_ + expression + rparen + expression

instantiation %= new_ + type_name + lparen + arguments + rparen

expression_block %= lbrace + expression_list + rbrace

expression_list %= expression + semicolon
expression_list %= standalone_expression
expression_list %= standalone_expression + expression_list
expression_list %= expression + semicolon + expression_list