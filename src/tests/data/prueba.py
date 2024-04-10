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
NUM_OF_TEST_CASES = 28

def single_test_case(test_case = 1, erroneo = False):
    if not erroneo:
        code = scripts[test_case]
    else:
        code = scripts_B[test_case]
    print("The code is")
    print(code)
    tokens = lexer(code)
    for token in tokens:
        token.token_type = G[token.token_type]
    tokens[-1].token_type = G.EOF
    #print("The tokens are:")
    #print(tokens)
    right_parse, operations = parser(tokens, get_shift_reduce= True, show= False)
    #print("The right parse obtained is")
    #print(right_parse)
    ast = evaluate_reverse_parse(right_parse, operations, tokens, synthetize_pure_tokens= True)
    formatter = FormatVisitor()
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
    errors.sort()
    errors = [("ERROR in line " + str(tpl[0]) + " " + tpl[1]) for tpl in errors]
    print("The context is:")
    print(type_checker.context)
    print("The errors are:")
    for error in errors:
        print(error)

def all_test_cases(erroneo = False):
    print("A continuacion uno tras otro un bulto de casos de prueba")
    for i in range(0, NUM_OF_TEST_CASES + 1):
        single_test_case(i, erroneo)
        input("Press Enter for the next Test_Case")
        print("____________________________________________________________________________")

#single_test_case(6)
all_test_cases()
#all_test_cases(True)