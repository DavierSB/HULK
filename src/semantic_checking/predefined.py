import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.semantic import Context, Method, VoidType, ErrorType, Type
from typing import Set

class AnyType(Type):
    def __init__(self):
        super().__init__('Any')
    
    def conforms_to(self, other):
        return True

def initialize_predefined_types(context : Context):
    context.create_type('Object')
    context.create_type('Number')
    context.create_type('Literal')
    context.create_type('Boolean')
    context.types['Any'] = AnyType()
    context.types['<void>'] = VoidType()
    context.types['error'] = ErrorType()
    object_type = context.types['Object']
    context.types['Number'].set_parent(object_type)
    context.types['Literal'].set_parent(object_type)
    context.types['Boolean'].set_parent(object_type)

def initialize_predefined_functions(context : Context, global_functions : Set[Method]):
    object_type = context.types['Object']
    number_type = context.types['Number']
    void_type = context.types['<void>']
    predefined_methods = [
        Method('print', ['value'], [object_type], void_type),
        Method('sin', ['value'], [number_type], number_type),
        Method('cos', ['value'], [number_type], number_type),
        Method('log', ['value'], [number_type], number_type),
        Method('sqrt', ['value'], [number_type], number_type),
        Method('exp', ['value'], [number_type], number_type),
        Method('rand', [], [], number_type)
    ]
    global_functions.update(set(predefined_methods))