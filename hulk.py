import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/lexer')
sys.path.insert(0, current_dir + '/src/parser')
from src.parser.slr1_parser import SLR1Parser
from src.parser.grammar import G
from src.lexer.lexer import lexer
from src.cmp.evaluation import evaluate_reverse_parse
from src.semantic_checking.visualization_visitor import FormatVisitor
from src.semantic_checking.type_collector_visitor import TypeCollectorVisitor
from src.semantic_checking.type_builder_visitor import TypeBuilderVisitor
from src.semantic_checking.type_checker_visitor import TypeCheckerVisitor
from src.interpreter.interpreter import Interpreter_Visitor
from src.cmp.semantic import Context, Scope

SHOW = False
DEBUG = False

parser = SLR1Parser(G)
file = open('A.hulk', 'r')
code = file.read()
tokens = lexer(code)
for token in tokens:
    token.token_type = G[token.token_type]
tokens[-1].token_type = G.EOF
if SHOW:
    print("The tokens are:")
    print(tokens)
right_parse, operations = parser(tokens, get_shift_reduce= True, show= False)
ast = evaluate_reverse_parse(right_parse, operations, tokens, synthetize_pure_tokens= True)
formatter = FormatVisitor()
if SHOW:
    print("The AST is:")
    print(formatter.visit(ast))
context = Context()
errors = []
type_collector = TypeCollectorVisitor(context, errors)
type_collector.visit(ast)
type_builder = TypeBuilderVisitor(context, errors)
type_builder.visit(ast)
type_checker = TypeCheckerVisitor(context, type_builder.global_functions, errors, DEBUG)
type_checker.visit(ast)
errors.sort()
errors = [("ERROR in line " + str(tpl[0]) + " " + tpl[1]) for tpl in errors]
if SHOW:
    print("The context is:")
    print(type_checker.context)
    print("The global functions are:")
    print(type_checker.global_functions)
if len(errors) > 0:
    print("The compilation errors are:")
    print(errors)
else:
    print("No Compilation Errors")
    intepreter = Interpreter_Visitor(type_checker.context, type_checker.global_functions, DEBUG)
    intepreter.visit(ast)