import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + 'src/semantic_checking')
import cmp.visitor as visitor
from semantic_checking.AST import *
from cmp.semantic import Context, Method, SemanticError, Type, ErrorType, VoidType
from semantic_checking.predefined import initialize_predefined_functions
from typing import List, Set

class TypeBuilderVisitor:
    def __init__(self, context: Context, errors : List[str]) -> None:
        self.context = context
        self.errors = errors
        self.type_being_build = None
        self.global_functions : Set[Method] = set()
        initialize_predefined_functions(self.context, self.global_functions)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode, args = None):
        for statement in node.statements:
            self.visit(statement)
            self.type_being_build = None
    
    @visitor.when(TypeDefinitionNode)
    def visit(self, node : TypeDefinitionNode, args = None):
        type_name = node.name.lex
        self.type_being_build : Type = self.context.types[type_name]
        if node.parent_name:
            parent_name = node.parent_name.lex
            try:
                parent = self.context.get_type(parent_name)
                self.type_being_build.set_parent(parent)
            except Exception as ex:
                self.errors.append((node.line, "The type " + parent_name + " is not defined"))
        
        for func in node.function_declarations:
            self.visit(func)
        
        constructor_parameter_names = []
        set_of_parameter_names = set()
        constructor_parameter_types = []
        for parameter in node.own_parameters:
            new_parameter_name = parameter.id.lex
            if new_parameter_name in set_of_parameter_names:
                self.errors.append((node.line, "All parameters must be named different"))
            set_of_parameter_names.add(new_parameter_name)
            constructor_parameter_names.append(new_parameter_name)
            try:
                new_parameter_type = self.context.get_type(parameter.type_annotation.lex)
            except Exception as ex:
                self.errors.append((node.line, ex.text))
                new_parameter_type = ErrorType()
            constructor_parameter_types.append(new_parameter_type)
        for attr in node.attribute_declarations:
            self.visit(attr)
        self.type_being_build.define_method("__constructor__", constructor_parameter_names, constructor_parameter_types, VoidType())
    
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node : FunctionDefinitionNode, args = None):
        parameter_names = [p.id.lex for p in node.parameters]
        parameter_types = []
        for parameter in node.parameters:
            try:
                type_name = parameter.type_annotation.lex
                parameter_types.append(self.context.get_type(type_name))
            except Exception as ex:
                self.errors.append((node.line, ex.text))
                parameter_types.append(ErrorType())
        
        try:
            return_type = node.type_annotation.lex
            return_type = self.context.get_type(return_type)
        except Exception as ex:
            self.errors.append((node.line, ex.text))
            return_type = ErrorType()

        if not self.type_being_build:
            method = Method(node.name.lex, parameter_names, parameter_types, return_type)
            if not method in self.global_functions:
                self.global_functions.add(method)
            else:
                self.errors.append((node.line, "Method " + node.name.lex + " with such parameters was already declared"))
        else:
            try:
                self.type_being_build.define_method(node.name.lex, parameter_names, parameter_types, return_type)
            except:
                self.errors.append((node.line, "Type " + self.type_being_build.name + " already has a definition for " + node.name.lex + " with such parameters"))
    
    @visitor.when(DeclarationNode)
    def visit(self, node: DeclarationNode, args = None):
        attr_name = node.id.lex
        try:
            attr_type = node.type_annotation.lex
            attr_type = self.context.get_type(attr_type)
        except Exception as ex:
            self.errors.append((node.line, ex.text))
            attr_type = ErrorType()
        try:
            self.type_being_build.define_attribute(attr_name, attr_type)
        except:
            self.errors.append((node.line, "Type " + self.type_being_build.name + " already has an attribute with the name " + attr_name))