import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/lexer')
sys.path.insert(0, current_dir + '/src/parser')
from src.parser.slr1_parser import SLR1Parser
from src.parser.grammar import G
from src.lexer.lexer import lexer
from scripts_de_prueba_semantic_check import scripts
from cmp.evaluation import evaluate_reverse_parse

parser = SLR1Parser(G)
tokens = lexer(scripts[3])
tokens_filtered = [G[token.token_type] for token in tokens]
tokens_filtered[-1] = G.EOF
right_parse, operations = parser(tokens_filtered, get_shift_reduce= True, show= False)
ast = evaluate_reverse_parse(right_parse, operations, tokens)
print(ast)