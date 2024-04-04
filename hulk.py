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
from src.cmp.semantic import Context, Scope 
from scripts_de_prueba import scripts
from scripts_de_prueba_con_errores import scripts_B

parser = SLR1Parser(G)

def single_test_case(test_case = 1, erroneo = False):
    if not erroneo:
        code = scripts[test_case]
    else:
        code = scripts_B[test_case]
    tokens = lexer(code)
    tokens_filtered = [G[token.token_type] for token in tokens]
    tokens_filtered[-1] = G.EOF
    right_parse, operations = parser(tokens_filtered, get_shift_reduce= True, show= False)
    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    formatter = FormatVisitor()
    print("The code is:")
    print(code)
    print("The AST is:")
    print(formatter.visit(ast))
    context = Context()
    errors = []
    type_collector = TypeCollectorVisitor(context, errors)
    type_collector.visit(ast)
    type_builder = TypeBuilderVisitor(context, errors)
    type_builder.visit(ast)
    type_checker = TypeCheckerVisitor(context, type_builder.global_functions, errors)
    type_checker.visit(ast)
    print(type_checker.errors)
    print("LLEGUEEEEE")

def all_test_cases(erroneo = False):
    print("A continuacion uno tras otro un bulto de casos de prueba")
    for i in range(0, 27):
        single_test_case(i, erroneo)
        input("Press Enter for the next Test_Case")
        print("____________________________________________________________________________")

#single_test_case(26)
all_test_cases()
#all_test_cases(True)