from typing import List, Tuple
from cmp.pycompiler import Production

registered_items = {}
registered_item_sets = {}

def assign_id_for_item(item_describer : Tuple[Production, int]) -> int:
    if item_describer in registered_items:
        return registered_items[item_describer]
    registered_items[item_describer] = len(registered_items)
    return registered_items[item_describer]

def assign_id_for_item_set(items : List):
    ids = [item.id for item in items]
    ids.sort()
    id = tuple(ids)
    if id in registered_item_sets:
        return registered_item_sets[id]
    registered_item_sets[id] = len(registered_item_sets)
    return registered_item_sets[id]