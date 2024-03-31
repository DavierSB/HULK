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
from scripts_de_prueba import scripts

parser = SLR1Parser(G)

def single_test_case(test_case = 1):
    code = scripts[test_case]
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

def all_test_cases():
    print("A continuacion uno tras otro un bulto de casos de prueba")
    for i in range(0, 23):
        single_test_case(i)
        input("Press Enter for the next Test_Case")
        print("____________________________________________________________________________")


all_test_cases()