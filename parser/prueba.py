from defining_grammar import grammar, ecuation
import parser

print(parser.parse_LR(ecuation, grammar))
