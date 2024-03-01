from items_register import assign_id_for_item, assign_id_for_item_set
from typing import List
from cmp.pycompiler import Grammar, Production, Sentence, Symbol


class Item:
    def __init__(self, production : Production, idx_of_point : int, contains_start_symbol = False) -> None:
        self.production = production
        self.idx_of_point = idx_of_point
        self.is_kernel = (idx_of_point > 0) or contains_start_symbol
        self.id = assign_id_for_item((self.production, self.idx_of_point))

    @property
    def seen(self):
        return self.production.Right[0: self.idx_of_point]
    
    @property
    def expected_sentence(self):
        return self.production.Right[self.idx_of_point:]
    
    @property
    def expected_symbol(self) -> Symbol:
        if self.idx_of_point < len(self.production.Right):
            return self.production.Right[self.idx_of_point]

    def read_symbol(self, symbol : Symbol) -> 'Item':
        if self.expected_symbol == symbol:
            return Item(self.production, self.idx_of_point + 1)

    def __str__(self) -> str:
        seen_str = ''.join(map(str, self.seen))
        expected_str = ''.join(map(str, self.expected_sentence))
        return str(self.production.Left) + ' -> ' + seen_str + '.' + expected_str
    
    def __repr__(self) -> str:
        return str(self)
    
    @staticmethod
    def all_items_from(production : Production, has_start_symbol = False) -> List['Item']:
        kernel_items = []
        not_kernel_items = []
        for i in range(len(production.Right) + 1):
            item = Item(production, i, has_start_symbol)
            if item.is_kernel:
                kernel_items.append(item)
            else:
                not_kernel_items.append(item)
        return kernel_items, not_kernel_items          

class Item_Set():
    def __init__(self, kernel_items : List[Item]):
        self.kernel_items = set(kernel_items)
        self.non_kernel_items = set()
        self.id = assign_id_for_item_set(self.kernel_items)
        self.items = self.kernel_items #por ahora

    def __len__(self):
        return len(self.items)

    def compute_closure(self, grammar : Grammar):
        len_before_expand = 0
        while len(self) > len_before_expand:
            len_before_expand = len(self)
            nonTerminals_to_expand = set()
            for item in self.items:
                if item.expected_symbol and item.expected_symbol.IsNonTerminal:
                    nonTerminals_to_expand.add(item.expected_symbol)
            for symbol in nonTerminals_to_expand:
                self.non_kernel_items.update(grammar.non_kernel_items[symbol])
            self.items = self.kernel_items.union(self.non_kernel_items)
    
    #De manera que read symbol solo puede ser realizado una vez que se ha hecho closure
    def read_symbol(self, symbol : Symbol):
        new_items = []
        for item in self.items:
            if item.expected_symbol:
                new_item = item.read_symbol(symbol)
                if new_item:
                    new_items.append(new_item)
        if len(new_items) > 0:
            return Item_Set(new_items)
        return None
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
    def __str__(self):
        aux_str = "\nid :" + str(self.id) + "\n"
        for item in self.kernel_items:
            aux_str = aux_str + str(item) + "\n"
        aux_str = aux_str + "\n"
        for item in self.non_kernel_items:
            aux_str = aux_str + str(item) + "\n"
        return aux_str + "\n\n\n"
    
    def __repr__(self):
        return str(self)