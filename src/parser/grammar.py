import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.pycompiler import Grammar
from semantic_checking.AST import *
G = Grammar()

#NonTerminals
program = G.NonTerminal('PROGRAM', True)
expression, statement = G.NonTerminals('EXPRESSION STATEMENT')
disjunction, conjunction, proposition, is_expression, boolean_term, concatenation, arithmetic_expression, sum_operator, factor, mult_operator, power_term, monomial, constant_term, term, casted_term = G.NonTerminals('DISJUNCTION CONJUNCTION PROPOSITION IS_EXPRESSION BOOLEAN_TERM CONCATENATION ARITHMETIC_EXPRESSION SUM_OPERATOR FACTOR MULT_OPERATOR POWER_TERM MONOMIAL CONSTANT_TERM TERM CASTED_TERM')
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
is_, as_ = G.Terminals('IS AS')
dot, colon, comma, semicolon = G.Terminals('DOT COLON COMMA SEMICOLON')
lparen, rparen, lbrace, rbrace = G.Terminals('LPAREN RPAREN LBRACE RBRACE')
lambda_, assign, reassign = G.Terminals('LAMBDA ASSIGN REASSIGN')
math_function, print_, constant = G.Terminals('MATH_FUNCTION PRINT CONSTANT')
let_, in_, function_ = G.Terminals('LET IN FUNCTION')
if_, else_, elif_, while_, for_, range_ = G.Terminals('IF ELSE ELIF WHILE FOR RANGE')
type_, self_, new_ = G.Terminals('TYPE SELF NEW')
inherits, protocol, extends = G.Terminals('INHERITS PROTOCOL EXTENDS')
predefined_type = G.Terminal('PREDEFINED_TYPE')

program %= expression + semicolon, lambda h, s: ProgramNode([], s[1], s[1].line)
program %= standalone_expression, lambda h, s: ProgramNode([], s[1], s[1].line)
program %= statement + program, lambda h, s: ProgramNode([s[1]] + s[2].statements, s[2].expression, s[1].line)

statement %= function_definition, lambda h, s: s[1]
statement %= type_definition, lambda h, s: s[1]

#Standalone Expression
standalone_expression %= let_ + declarations + in_ + standalone_expression, lambda h, s: LetNode(s[2], s[4], s[1].line)
standalone_expression %= if_ + if_body + else_ + standalone_expression, lambda h, s: IfNode(s[2].conditions, s[2].expressions, s[4], s[1].line)
standalone_expression %= while_ + lparen + expression + rparen + standalone_expression, lambda h, s: WhileNode(s[3], s[5], s[1].line)
standalone_expression %= for_ + lparen + id + type_annotation + in_ + expression + rparen + standalone_expression, lambda h, s: ForNode(IDNode(s[3].lex), s[4], s[6], s[8], s[1].line)
standalone_expression %= expression_block, lambda h, s: s[1]

#Expression
expression %= disjunction, lambda h, s: s[1]
expression %= let_expression, lambda h, s: s[1]
expression %= if_expression, lambda h, s: s[1]
expression %= while_expression, lambda h, s: s[1]
expression %= for_expression, lambda h, s: s[1]
expression %= instantiation, lambda h, s: s[1]
expression %= reassignable + reassign + expression, lambda h, s: ReassignNode(s[1], s[3], s[1].line)
expression %= expression_block, lambda h, s: s[1]

#Simple Expression
disjunction %= conjunction, lambda h, s: s[1]
disjunction %= conjunction + or_ + disjunction, lambda h, s: OrNode(s[1], s[3], s[1].line)

conjunction %= proposition, lambda h, s: s[1]
conjunction %= proposition + and_ + conjunction, lambda h, s: AndNode(s[1], s[3], s[1].line)

proposition %= is_expression, lambda h, s: s[1]
proposition %= not_ + proposition, lambda h, s: NotNode(s[2], s[1].line)

is_expression %= boolean_term, lambda h, s: s[1]
is_expression %= boolean_term + is_ + type_name, lambda h, s: IsNode(s[1], s[3], s[1].line)

boolean_term %= concatenation, lambda h, s: s[1]
boolean_term %= concatenation + comparer + boolean_term, lambda h, s: ComparerNode(s[1], s[3], s[2].lex, s[1].line)

concatenation %= arithmetic_expression, lambda h, s: s[1]
concatenation %= arithmetic_expression + concat + concatenation, lambda h, s: ConcatNode(s[1], s[3], s[2].lex, s[1].line)

arithmetic_expression %= factor, lambda h, s: s[1]
arithmetic_expression %= factor + sum_operator + arithmetic_expression, lambda h, s: ArithmeticNode(s[1], s[3], s[2].lex, s[1].line)

sum_operator %= plus, lambda h, s: s[1]
sum_operator %= minus, lambda h, s: s[1]

factor %= power_term, lambda h, s: s[1]
factor %= power_term + mult_operator + factor, lambda h, s: ArithmeticNode(s[1], s[3], s[2].lex, s[1].line)

mult_operator %= times, lambda h, s: s[1]
mult_operator %= divide, lambda h, s: s[1]
mult_operator %= module, lambda h, s: s[1]

power_term %= monomial, lambda h, s: s[1]
power_term %= monomial + power + power_term, lambda h, s: ArithmeticNode(s[1], s[3], s[2].lex, s[1].line)

monomial %= term, lambda h, s: s[1]
monomial %= minus + term, lambda h, s: ArithmeticNode(NumberNode('0'), s[2], '-', s[1].line)

term %= casted_term, lambda h, s: s[1]
term %= casted_term + as_ + type_name, lambda h, s: AsNode(s[1], s[3], s[1].line)

casted_term %= number, lambda h, s: NumberNode(s[1].lex, s[1].line)
casted_term %= constant, lambda h, s: NumberNode('3.14', s[1].line) if s[1] == 'PI' else NumberNode('2.72', s[1].line)
casted_term %= literal, lambda h, s: LiteralNode(s[1].lex, s[1].line)
casted_term %= boolean, lambda h, s: BooleanNode(s[1].lex, s[1].line)
casted_term %= reassignable, lambda h, s: s[1]
casted_term %= not_reassignable, lambda h, s: s[1]

reassignable %= end_of_reassignable, lambda h, s: s[1]
reassignable %= self_ + dot + end_of_reassignable, lambda h, s: MemberNode(SelfNode(), s[3], s[1].line)
reassignable %= lparen + expression + rparen + end_of_reassignable, lambda h, s: MemberNode(s[2], s[4], s[1].line)

end_of_reassignable %= id, lambda h, s: IDNode(s[1].lex, s[1].line)
end_of_reassignable %= id + dot + end_of_reassignable, lambda h, s: MemberNode(IDNode(s[1].lex, s[1].line), s[3], s[1].line)
end_of_reassignable %= function_call + dot + end_of_reassignable, lambda h, s: MemberNode(s[1], s[3], s[1].line)

not_reassignable %= end_of_not_reassignable, lambda h, s: s[1]
not_reassignable %= self_ + dot + end_of_not_reassignable, lambda h, s: MemberNode(SelfNode(s[1].line), s[3], s[1].line)
not_reassignable %= lparen + expression + rparen, lambda h, s: s[2]
not_reassignable %= lparen + expression + rparen + end_of_not_reassignable, lambda h, s: MemberNode(s[2], s[4], s[1].line)

end_of_not_reassignable %= function_call, lambda h, s: s[1]
end_of_not_reassignable %= id + dot + end_of_not_reassignable, lambda h, s: MemberNode(IDNode(s[1].lex, s[1].line), s[3], s[1].line)
end_of_not_reassignable %= function_call + dot + end_of_not_reassignable, lambda h, s: MemberNode(s[1], s[3], s[1].line)

function_call %= function_name + lparen + arguments + rparen, lambda h, s: FunctionCallNode(s[1], s[3], s[1].line)

function_name %= id, lambda h, s: FunctionNameNode(s[1].lex, s[1].line)
function_name %= math_function, lambda h, s: FunctionNameNode(s[1].lex, s[1].line)
function_name %= print_, lambda h, s: FunctionNameNode(s[1].lex, s[1].line)
function_name %= range_, lambda h, s: FunctionNameNode(s[1].lex, s[1].line)

arguments %= expression + comma + arguments, lambda h, s: [s[1]] + s[3]
arguments %= expression, lambda h, s: [s[1]]
arguments %= G.Epsilon, lambda h, s: []

#Let
let_expression %= let_ + declarations + in_ + expression, lambda h, s: LetNode(s[2], s[4], s[1].line)

declarations %= id + type_annotation + assign + expression, lambda h, s: [DeclarationNode(IDNode(s[1].lex, s[1].line), s[2], s[4], s[1].line)]
declarations %= id + type_annotation + assign + expression + comma + declarations, lambda h, s: [DeclarationNode(IDNode(s[1].lex, s[1].line), s[2], s[4], s[1].line)] + s[6]

#Type_annotation
type_annotation %= colon + type_name, lambda h, s: s[2]
type_annotation %= G.Epsilon, lambda h, s: TypeNameNode() #Como rayos paso las coordenadas aqui?

type_name %= id, lambda h, s: TypeNameNode(s[1].lex, s[1].line)
type_name %= predefined_type, lambda h, s: TypeNameNode(s[1].lex, s[1].line)

#If
if_expression %= if_ + if_body + else_ + expression, lambda h, s: IfNode(s[2].conditions, s[2].expressions, s[4], s[1].line)

if_body %= lparen + expression + rparen + expression, lambda h, s: IfNode([s[2]], [s[4]], None, s[1].line)
if_body %= lparen + expression + rparen + expression + elif_ + if_body, lambda h, s: IfNode([s[2]] + s[6].conditions, [s[4]] + s[6].expressions, None, s[1].line)

#Loops
while_expression %= while_ + lparen + expression + rparen + expression, lambda h, s: WhileNode(s[3], s[5], s[1].line)

for_expression %= for_ + lparen + id + type_annotation + in_ + expression + rparen + expression, lambda h, s: ForNode(IDNode(s[3].lex, s[1].line), s[4], s[6], s[8], s[1].line)

#Instantiation
instantiation %= new_ + type_name + lparen + arguments + rparen, lambda h, s: NewNode(s[2], s[4], s[1].line)

#Expression_block
expression_block %= lbrace + expression_list + rbrace, lambda h, s: ExpressionBlockNode(s[2], s[1].line)

expression_list %= expression + semicolon, lambda h, s: [s[1]]
expression_list %= standalone_expression, lambda h, s: [s[1]]
expression_list %= standalone_expression + expression_list, lambda h, s: [s[1]] + s[2]
expression_list %= expression + semicolon + expression_list, lambda h, s: [s[1]] + s[3]

#Function definition
function_definition %= function_ + function_definition_body, lambda h, s: s[2]

function_definition_body %= id + lparen + parameters + rparen + type_annotation + function_body, lambda h, s: FunctionDefinitionNode(FunctionNameNode(s[1].lex, s[1].line), s[3], s[5], s[6], s[1].line)

function_body %= lambda_ + expression_for_inline_function + semicolon, lambda h, s: s[2]
function_body %= expression_block, lambda h, s: s[1]

expression_for_inline_function %= disjunction, lambda h, s: s[1]
expression_for_inline_function %= let_expression, lambda h, s: s[1]
expression_for_inline_function %= if_expression, lambda h, s: s[1]
expression_for_inline_function %= while_expression, lambda h, s: s[1]
expression_for_inline_function %= for_expression, lambda h, s: s[1]
expression_for_inline_function %= instantiation, lambda h, s: s[1]
expression_for_inline_function %= reassignable + reassign + expression_for_inline_function, lambda h, s: ReassignNode(s[1], s[3], s[1].line)

parameters %= G.Epsilon, lambda h, s: []
parameters %= id + type_annotation, lambda h, s: [ParameterNode(IDNode(s[1].lex, s[1].line), s[2], s[1].line)]
parameters %= id + type_annotation + comma + parameters, lambda h, s: [ParameterNode(IDNode(s[1].lex, s[1].line), s[2], s[1].line)] + s[4]

#Type definition
#Solo permitimos dos formas de definir tipos:
#con los parametros por default, o sea, no se especifican los de la clase o su padre
#especificando los parametros del tipo y de su padre
type_definition %= type_ + id + type_block, lambda h, s: TypeDefinitionNode(TypeNameNode(s[2].lex, s[1].line), [], None, None, s[3], s[1].line)
type_definition %= type_ + id + lparen + parameters + rparen + type_block, lambda h, s: TypeDefinitionNode(TypeNameNode(s[2].lex, s[1].line), s[4], None, None, s[6], s[1].line)
type_definition %= type_ + id + inherits + type_name + type_block, lambda h, s: TypeDefinitionNode(TypeNameNode(s[2].lex, s[1].line), [], s[4], [], s[5], s[1].line)
type_definition %= type_ + id + lparen + parameters + rparen + inherits + type_name + lparen + arguments + rparen + type_block, lambda h, s: TypeDefinitionNode(TypeNameNode(s[2].lex, s[1].line), s[4], s[7], s[9], s[11], s[1].line)

type_block %= lbrace + internal_declarations + rbrace, lambda h, s: s[2]

internal_declarations %= G.Epsilon, lambda h, s: ([], [])
internal_declarations %= id + type_annotation + assign + expression + semicolon + internal_declarations, lambda h, s: ([DeclarationNode(IDNode(s[1].lex, s[1].line), s[2], s[4], s[1].line)] + s[6][0], s[6][1])
internal_declarations %= id + type_annotation + assign + standalone_expression + internal_declarations, lambda h, s: ([DeclarationNode(IDNode(s[1].lex, s[1].line), s[2], s[4], s[1].line)] + s[6][0], s[6][1])
internal_declarations %= function_definition_body + internal_declarations, lambda h, s: (s[2][0], [s[1]] + s[2][1])