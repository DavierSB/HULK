from typing import Dict, List, Tuple
from cmp.pycompiler import Grammar, Symbol, Sentence, Production
from calculate_firsts import calculate_firsts_for_symbols, calculate_firsts_for_sentence
from calculate_follows import calculate_follows
from items import Item, Item_Set

class Grammar_LL(Grammar):
    def __init__(self):
        super().__init__()
        self.firsts : Dict[Symbol, List[Symbol]]
        self.follows : Dict[Symbol, List[Symbol]]
    
    def initialize(self) -> None:
        calculate_firsts_for_symbols(self)
        calculate_follows(self)
    
    def calculate_firsts_for_sentence(self, sentence : Sentence) -> List[Symbol]:
        return calculate_firsts_for_sentence(sentence, self)
    
    def get_table(self) -> Dict[Tuple[Symbol, Symbol], Production]:
        table = {}
        for production in self.Productions:
            nt = production.Left
            if production.IsEpsilon:
                for t in self.follows[nt]:
                    table[(nt, t)] = production
            for t in self.calculate_firsts_for_sentence(production.Right):
                table[(nt, t)] = production
        return table

class Grammar_LR(Grammar_LL):
    def __init__(self):
        super().__init__()
        self.kernel_items : Dict[Symbol, List[Item]]
        self.non_kernel_items : Dict[Symbol, List[Item]]
    
    def initialize(self):
        self.augment_grammar()
        super().initialize()
        self.load_items()
        self.compute_canonical_collection_of_items_sets_for_LR0()
    
    def augment_grammar(self):
        E = self.startSymbol
        self.startSymbol = None
        foolE = self.NonTerminal('E\'', True)
        foolE %= E
    
    def load_items(self) -> None:
        self.kernel_items = {}
        self.non_kernel_items = {}
        for nt in self.nonTerminals:
            self.kernel_items[nt] = []
            self.non_kernel_items[nt] = []
        production_id = 0
        for production in self.Productions:
            new_kernel_items, new_not_kernel_items = Item.all_items_from(production, production.Left == self.startSymbol)
            self.kernel_items[production.Left] = self.kernel_items[production.Left] + new_kernel_items
            self.non_kernel_items[production.Left] = self.non_kernel_items[production.Left] + new_not_kernel_items
    
    def compute_canonical_collection_of_items_sets_for_LR0(self):
        initial_set = Item_Set([self.kernel_items[self.startSymbol][0]])
        ccits = {0 : initial_set}
        go_to = {initial_set.id : {}}
        idx = 0
        while idx < len(ccits):
            ccits[idx].compute_closure(self)
            src_item_set = ccits[idx]
            for symbol in (self.terminals + self.nonTerminals):
                dest_item_set = src_item_set.read_symbol(symbol)
                if dest_item_set:
                    if dest_item_set.id in ccits:
                        go_to[src_item_set.id][symbol] = dest_item_set.id
                    else:
                        ccits[dest_item_set.id] = dest_item_set
                        go_to[dest_item_set.id] = {}
                        go_to[src_item_set.id][symbol] = dest_item_set.id
            idx = idx + 1
        self.ccits = ccits
        self.go_to = go_to



    def get_table(self):
        pass