import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/lexer')
sys.path.insert(0, current_dir + '/src/parser')
#print(sys.path)
#input()
from src.parser.slr1_parser import SLR1Parser
from src.parser.grammar import G
from src.lexer.lexer import lexer
from scripts_de_prueba import scripts

parser = SLR1Parser(G)
tokens = lexer(scripts[22])
tokens_filtered = [G[token.token_type] for token in tokens]
tokens_filtered[-1] = G.EOF
right_parse, operations = parser(tokens_filtered, get_shift_reduce= True, show= False)
for production in right_parse:
    print(production)