import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + '/src/semantic_checking')
from cmp.semantic import Context, Method, VoidType, ErrorType, AnyType, Type
from semantic_checking.AST import PredefinedFunctionNode, VoidNode, ExpressionBlockNode
from typing import Set

def initialize_predefined_types(context : Context):
    context.create_type('Object')
    context.create_type('Constant')
    context.create_type('Number')
    context.create_type('Literal')
    context.create_type('Boolean')
    context.types['Any'] = AnyType()
    context.types['<void>'] = VoidType()
    context.types['error'] = ErrorType()
    object_type : Type = context.types['Object']
    object_type.define_method('__constructor__', [], [], VoidType(), ExpressionBlockNode([], -1))
    constant_type = context.types['Constant']
    constant_type.set_parent(object_type)
    context.types['Number'].set_parent(constant_type)
    context.types['Literal'].set_parent(constant_type)
    context.types['Boolean'].set_parent(constant_type)

def initialize_predefined_functions(context : Context, global_functions : Set[Method]):
    object_type = context.types['Object']
    number_type = context.types['Number']
    void_type = context.types['<void>']
    predefined_methods = [
        Method('print', ['value'], [object_type], void_type, PredefinedFunctionNode('print', -1)),
        Method('sin', ['value'], [number_type], number_type, PredefinedFunctionNode('sin', -1)),
        Method('cos', ['value'], [number_type], number_type, PredefinedFunctionNode('cos', -1)),
        Method('log', ['value'], [number_type], number_type, PredefinedFunctionNode('log', -1)),
        Method('log', ['value', 'base'], [number_type, number_type], number_type, PredefinedFunctionNode('log', -1)),
        Method('sqrt', ['value'], [number_type], number_type, PredefinedFunctionNode('sqrt', -1)),
        Method('exp', ['value'], [number_type], number_type, PredefinedFunctionNode('exp', -1)),
        Method('rand', [], [], number_type, PredefinedFunctionNode('rand', -1))
    ]
    global_functions.update(set(predefined_methods))