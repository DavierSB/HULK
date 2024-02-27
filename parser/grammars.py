from typing import Dict, List, Tuple
from cmp.pycompiler import Grammar, Symbol, Sentence, Production
from calculate_firsts import calculate_firsts_for_symbols, calculate_firsts_for_sentence
from calculate_follows import calculate_follows
from items import Item

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
        self.n_of_kernel_items = 0
    
    def initialize(self):
        self.add_fool_start_state()
        super().initialize()
        self.load_items()
    
    def add_fool_start_state(self):
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
        for production in self.Productions:
            new_kernel_items, new_not_kernel_items = Item.all_items_from(production)
            for item in new_kernel_items:
                item.id = self.n_of_kernel_items
                self.n_of_kernel_items = self.n_of_kernel_items + 1
            self.kernel_items[production.Left] = self.kernel_items[production.Left] + new_kernel_items
            self.non_kernel_items[production.Left] = self.non_kernel_items[production.Left] + new_not_kernel_items

    def get_table(self):
        pass