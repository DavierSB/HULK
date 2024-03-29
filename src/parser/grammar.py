import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.pycompiler import Grammar
G = Grammar()

#NonTerminals
program = G.NonTerminal('PROGRAM', True)
expression, statement = G.NonTerminals('EXPRESSION STATEMENT')
disjunction, conjunction, proposition, boolean_term, concatenation, arithmetic_expression, sum_operator, factor, mult_operator, power_term, monomial, constant_term, term = G.NonTerminals('DISJUNCTION CONJUNCTION PROPOSITION BOOLEAN_TERM CONCATENATION ARITHMETIC_EXPRESSION SUM_OPERATOR FACTOR MULT_OPERATOR POWER_TERM MONOMIAL CONSTANT_TERM TERM')
reassignable, not_reassignable, end_of_reassignable, end_of_not_reassignable = G.NonTerminals('REASSIGNABLE NOT_REASSIGNABLE END_OF_REASSIGNABLE END_OF_NOT_REASSIGNABLE')
function_call, function_name, arguments = G.NonTerminals('FUNCTION_CALL FUNCTION_NAME ARGUMENTS')
let_expression, declarations, type_annotation, type_name = G.NonTerminals('LET_EXPRESSION DECLARATIONS TYPE_ANNOTATION TYPE_NAME')
if_expression, if_body = G.NonTerminals('IF_EXPRESSION IF_BODY')
while_expression, for_expression, instantiation = G.NonTerminals('WHILE_EXPRESSION FOR_EXPRESSION INSTANTIATION')
expression_block, expression_list = G.NonTerminals('EXPRESSION_BLOCK EXPRESSION_LIST')
standalone_expression = G.NonTerminal('STANDALONE_EXPRESSION')
function_definition, function_definition_body, function_body, expression_for_inline_function, parameters = G.NonTerminals('FUNCTION_DEFINITION FUNCTION_DEFINITION_BODY FUNCTION_BODY EXPRESSION_FOR_INLINE_FUNCTION PARAMETERS')
type_definition, type_block, internal_declarations = G.NonTerminals('TYPE_DEFINITION, TYPE_BLOCK, INTERNAL_DECLARATIONS')

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

statement %= function_definition
statement %= type_definition

#Standalone Expression
standalone_expression %= let_ + declarations + in_ + standalone_expression
standalone_expression %= if_ + if_body + else_ + standalone_expression
standalone_expression %= while_ + lparen + expression + rparen + standalone_expression
standalone_expression %= for_ + lparen + id + type_annotation + in_ + expression + rparen + standalone_expression
standalone_expression %= expression_block

#Expression
expression %= disjunction
expression %= let_expression
expression %= if_expression
expression %= while_expression
expression %= for_expression
expression %= instantiation
expression %= reassignable + reassign + expression
expression %= expression_block

#Simple Expression
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
term %= reassignable
term %= not_reassignable

reassignable %= end_of_reassignable
reassignable %= self_ + dot + end_of_reassignable
reassignable %= lparen + expression + rparen + end_of_reassignable

end_of_reassignable %= id
end_of_reassignable %= id + dot + end_of_reassignable
end_of_reassignable %= function_call + dot + end_of_reassignable

not_reassignable %= end_of_not_reassignable
not_reassignable %= self_ + dot + end_of_not_reassignable
not_reassignable %= lparen + expression + rparen
not_reassignable %= lparen + expression + rparen + end_of_not_reassignable

end_of_not_reassignable %= function_call
end_of_not_reassignable %= id + dot + end_of_not_reassignable
end_of_not_reassignable %= function_call + dot + end_of_not_reassignable

function_call %= function_name + lparen + arguments + rparen

function_name %= id
function_name %= math_function
function_name %= print_
function_name %= range_

arguments %= expression + comma + arguments
arguments %= expression
arguments %= G.Epsilon

#Let
let_expression %= let_ + declarations + in_ + expression

declarations %= id + type_annotation + assign + expression
declarations %= id + type_annotation + assign + expression + comma + declarations

#Type_annotation
type_annotation %= colon + type_name
type_annotation %= G.Epsilon

type_name %= id
type_name %= predefined_type

#If
if_expression %= if_ + if_body + else_ + expression

if_body %= lparen + expression + rparen + expression
if_body %= lparen + expression + rparen + expression + elif_ + if_body

#Loops
while_expression %= while_ + lparen + expression + rparen + expression

for_expression %= for_ + lparen + id + type_annotation + in_ + expression + rparen + expression

#Instantiation
instantiation %= new_ + type_name + lparen + arguments + rparen

#Expression_block
expression_block %= lbrace + expression_list + rbrace

expression_list %= expression + semicolon
expression_list %= standalone_expression
expression_list %= standalone_expression + expression_list
expression_list %= expression + semicolon + expression_list

#Function definition
function_definition %= function_ + function_definition_body

function_definition_body %= id + lparen + parameters + rparen + type_annotation + function_body

function_body %= lambda_ + expression_for_inline_function + semicolon
function_body %= expression_block

expression_for_inline_function %= disjunction
expression_for_inline_function %= let_expression
expression_for_inline_function %= if_expression
expression_for_inline_function %= while_expression
expression_for_inline_function %= for_expression
expression_for_inline_function %= instantiation
expression_for_inline_function %= reassignable + reassign + expression_for_inline_function

parameters %= G.Epsilon
parameters %= id + type_annotation
parameters %= id + type_annotation + comma + parameters

#Type definition
type_definition %= type_ + id + type_block
type_definition %= type_ + id + lparen + parameters + rparen + type_block
type_definition %= type_ + id + inherits + type_name + type_block
type_definition %= type_ + id + lparen + parameters + rparen + inherits + type_name + type_block
type_definition %= type_ + id + lparen + parameters + rparen + inherits + type_name + lparen + arguments + rparen + type_block

type_block %= lbrace + internal_declarations + rbrace

internal_declarations %= G.Epsilon
internal_declarations %= id + type_annotation + assign + expression + semicolon + internal_declarations
internal_declarations %= id + type_annotation + assign + standalone_expression + internal_declarations
internal_declarations %= function_definition_body + internal_declarations