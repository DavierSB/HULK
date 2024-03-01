from defining_grammar import grammar_LR
from items_register import registered_item_sets


grammar = grammar_LR()
grammar.initialize()

print(grammar.ccits)
print(grammar.go_to)