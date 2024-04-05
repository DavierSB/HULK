import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + 'src/semantic_checking')
import cmp.visitor as visitor
from semantic_checking.AST import *
from semantic_checking.predefined import initialize_predefined_types
from cmp.semantic import Context, SemanticError
from typing import List, Set

class TypeCollectorVisitor:
    def __init__(self, context : Context, errors : List[str]) -> None:
        self.context = context
        self.errors = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode):
        initialize_predefined_types(self.context)
        for statement in node.statements:
            self.visit(statement)
    
    @visitor.when(TypeDefinitionNode)
    def visit(self, node : TypeDefinitionNode):
        type_name = node.name.lex
        try:
            self.context.create_type(type_name)
        except SemanticError as ex:
            self.errors.append((node.line, ex.text))