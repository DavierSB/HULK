from typing import List
from cmp.pycompiler import Grammar, Production, Sentence, Symbol
class Item:
    def __init__(self, production : Production, idx_of_point : int, grammar : Grammar) -> None:
        self.production = production
        self.idx_of_point = idx_of_point
        self.is_kernel = (idx_of_point > 0) or (self.production.Left == grammar.startSymbol)
        self.id : int  #Los items kernel tienen un id que los identifica. Es asignado por la gramatia luego

    @property
    def seen(self):
        return self.production[0: self.idx_of_point]
    
    @property
    def expected_sentence(self):
        return self.production[self.idx_of_point:]
    
    @property
    def expected_character(self):
        if self.idx_of_point < len(self.production):
            return self.production[self.idx_of_point]

    def read_symbol(self, symbol : Symbol) -> 'Item':
        if self.expected_character == symbol:
            return Item(self.production, self.idx_of_point + 1)

    def __str__(self) -> str:
        seen_str = ''.join(map(str, self.seen))
        expected_str = ''.join(map(str, self.expected_sentence))
        return str(self.Left) + ' -> ' + seen_str + '.' + expected_str
    
    def __repr__(self) -> str:
        return str(self)
    
    @staticmethod
    def all_items_from(production : Production) -> List['Item']:
        kernel_items = []
        not_kernel_items = []
        for i in range(len(production.Right) + 1):
            item = Item(production, i)
            if item.isKernel:
                kernel_items.append(item)
            else:
                not_kernel_items.append(item)
        return kernel_items, not_kernel_items          

class Item_Set():
    def __init__(self, items : List[Item]):
        self.items = set(items)
        self.id = calculate_id_for_item_set(filter(lambda x : x.is_kernel, self.items))

    def __len__(self):
        return len(self.items)

    def compute_closure(self, grammar : Grammar):
        len_before_expand = 0
        while len(self) > len_before_expand:
            len_before_expand = len(self)
            nonTerminals_to_expand = set()
            for item in self.items:
                if item.expected_character and item.expected_character.isNonTerminal:
                    nonTerminals_to_expand.add(item.expected_character)
            for symbol in nonTerminals_to_expand:
                self.items.update(grammar.non_kernel_items[symbol])
    
    def read_symbol(self, symbol : Symbol):
        new_items = []
        for item in self.items:
            if item.expected_character:
                new_item = item.read_symbol(symbol)
                if new_item:
                    new_items.append(new_item)
        if len(new_items) > 0:
            return Item_Set(new_items)
        return None
    
    def __str__(self):
        return str(self.items)
    
    def __repr__(self):
        return repr(self.items)

def calculate_id_for_item_set(items : List[Item]):
    ids = []
    for item in items:
        ids.append(item.id)
    ids.sort()
    return int(''.join(map(str, ids)))