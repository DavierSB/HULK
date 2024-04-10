import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + 'src/semantic_checking')
sys.path.insert(0, current_dir + '/src/interpreter')
import cmp.visitor as visitor
from cmp.semantic import Context, Method, Scope, Type, VariableInfo
from semantic_checking.AST import *
from typing import Set, Dict
from random import random
import math

WRONG_DOWNCASTING = 'Error Line "%s": Cannot downcast "%s" to "%s"'

class Object_Instance:
    def __init__(self, type : Type, value = None):
        self.type = type
        self.scope = Scope()
        self.value = None
    
    def get_attribute(self, name : str):
        #No tengo problemas con que se levante una excepcion aqui, me parece bien
        self.type.get_attribute(name)
        return self.scope.find_variable(name).value
    
    def set_attribute(self, name : str, value):
        self.type.get_attribute(name)
        self.scope.find_variable(name).value = value

    def instantiate(self, arguments : List[VariableInfo], interpreter : 'Interpreter_Visitor'):
        scope = Scope()
        for var in arguments:
            scope.define_variable(var.name, var.type, var.value)
        
        constructor = self.type.get_method('__constructor__')
        for declaration in constructor.expression.expressions:
            declaration : DeclarationNode = declaration
            name = declaration.id.lex
            type = declaration.expression.inferred_type
            value = interpreter.visit(declaration.expression, scope.create_child())
            self.scope.define_variable(name, type, value)
        
        if self.type.parent:
            parent_instance = Object_Instance(self.type.parent)
            parent_arguments = constructor.expression.parent_arguments #La carta bajo la manga
            parent_constructor = self.type.parent.get_method('__constructor__')
            parent_param_values = interpreter.process_arguments(parent_arguments, parent_constructor, scope)
            parent_instance.instantiate(parent_param_values, interpreter)
            for var in parent_instance.scope.locals:
                if not self.scope.is_local(var.name):
                    self.scope.define_variable(var.name, var.type, var.value)
            #la recursividad solita traera todos los atributos de los padres

    def evaluate_method(self, name : str, arguments : List[VariableInfo], interpreter : 'Interpreter_Visitor'):
        previous_owner = interpreter.owner
        interpreter.owner = self
        method : Method = self.type.get_method(name)
        scope = Scope()
        for var in arguments:
            scope.define_variable(var.name, var.type, var.value)
        return_value = interpreter.visit(method.expression, scope)
        interpreter.owner = previous_owner
        return return_value

class Interpreter_Visitor:
    def __init__(self, context : Context, global_functions : Set[Method], show = False):
        self.context = context
        self.global_functions = global_functions
        self.owner = None
        self.show = show
    
    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode, scope : Scope = None):
        if self.show:print("Visited Program Node")
        if not scope:
            scope = Scope()
        return self.visit(node.expression, scope)
    
    @visitor.when(DeclarationNode)
    def visit(self, node : DeclarationNode, scope : Scope):
        if self.show:print("Visited Declaration Node")
        type = node.expression.inferred_type
        value = self.visit(node.expression, scope.create_child())
        scope.define_variable(node.id.lex, type, value)
    
    @visitor.when(ReassignNode)
    def visit(self, node : ReassignNode, scope : Scope):
        if self.show:print("Visited Reassign Node")
        value = self.visit(node.right, scope.create_child())
        if isinstance(node.left, MemberNode):
            owner_of_attribute : Object_Instance = self.visit(node.left.left, scope.create_child())
            var_name = node.left.right.lex #node.left.right es un IDNode (o explotaba el checker) 
            owner_of_attribute.set_attribute(var_name, value)
        else:#En este caso node.left es un IDNode
            var_name = node.left.lex
            scope.find_variable(var_name).value = value
        return value
    
    @visitor.when(ExpressionBlockNode)
    def visit(self, node : ExpressionBlockNode, scope : Scope):
        if self.show:print("Visited Expression Block Node")
        value = None
        for expression in node.expressions:
            value = self.visit(expression, scope.create_child())
        return value
    
    @visitor.when(LetNode)
    def visit(self, node : LetNode, scope : Scope):
        if self.show:print("Visited LetNode")
        for declaration in node.declarations:
            self.visit(declaration, scope)
        return self.visit(node.expression, scope)
    
    @visitor.when(IfNode)
    def visit(self, node : IfNode, scope : Scope):
        if self.show:print("Visited IfNode")
        idx = 0
        for condition in node.conditions:
            if self.visit(condition, scope.create_child()):
                return self.visit(node.expressions[idx], scope.create_child())
            else:
                idx += 1
        return self.visit(node.else_case, scope.create_child())
    
    @visitor.when(ForNode)
    def visit(self, node : ForNode, scope : Scope):
        raise NotImplementedError
    
    @visitor.when(WhileNode)
    def visit(self, node : WhileNode, scope : Scope):
        if self.show:print("Visited WhileNode")
        value = None
        while self.visit(node.condition, scope.create_child()):
            value = self.visit(node.expression, scope.create_child())
        return value
    
    def process_arguments(self, arguments : List[ExpressionNode], method : Method, scope : Scope) -> List[VariableInfo]:
        """Here we transform arguments in form of ExpressionNode into the declaration of
        parameters to pass to a function, in form of VariableInfo"""
        scope = scope.create_child()#por si acaso
        for i in range(len(arguments)):
            argument = arguments[i]
            value = self.visit(argument, scope.create_child())
            var_name = method.param_names[i]
            scope.define_variable(var_name, argument.inferred_type, value)
        return scope.locals

    @visitor.when(NewNode)
    def visit(self, node : NewNode, scope : Scope):
        if self.show:print("Visited NewNode")
        type_to_instantiate = node.inferred_type
        constructor : Method = type_to_instantiate.get_method('__constructor__')
        arguments = self.process_arguments(node.arguments, constructor, scope.create_child())
        
        new_instance = Object_Instance(type_to_instantiate)
        new_instance.instantiate(arguments, self)
        return new_instance
    
    @visitor.when(MemberNode)
    def visit(self, node : MemberNode, scope : Scope):
        if self.show:print("Visited MemberNode")
        object_instance : Object_Instance = self.visit(node.left, scope.create_child())
        if isinstance(node.right, FunctionCallNode):
            func_name = node.right.name.lex
            method = object_instance.type.get_method(func_name)
            arguments = self.process_arguments(node.right.arguments, method, scope)
            return object_instance.evaluate_method(func_name, arguments, self)
        else:
            return object_instance.get_attribute(node.right.lex)
    
    #Constant Values
    @visitor.when(IDNode)
    def visit(self, node : IDNode, scope : Scope, args = None):
        if self.show:print("Visited IDNode")
        return scope.find_variable(node.lex).value
    
    @visitor.when(SelfNode)
    def visit(self, node : SelfNode, scope : Scope, args = None):
        if self.show:print("Visited Self Node")
        return self.owner
    
    @visitor.when(NumberNode)
    def visit(self, node : NumberNode, scope : Scope, args = None):
        if self.show:print("Visited Number Node")
        return float(node.lex)
    
    @visitor.when(LiteralNode)
    def visit(self, node : LiteralNode, scope : Scope, args = None):
        if self.show:print("Visited Literal Node")
        return node.lex[1 : -1]
    
    @visitor.when(BooleanNode)
    def visit(self, node : BooleanNode, scope : Scope, args = None):
        if self.show:print("Visited Boolean Node")
        return bool(self.lex)

    @visitor.when(FunctionCallNode)
    def visit(self, node : FunctionCallNode, scope : Scope):
        if self.show:print("Visited FunctionCallNode")
        #Solo llegara aqui si la funcion que esta siendo llamada es global
        method = node.method
        for var in self.process_arguments(node.arguments, method, scope):
            scope.define_variable(var.name, var.type, var.value)
        return self.visit(method.expression, scope.create_child())
    
    @visitor.when(OrNode)
    def visit(self, node : OrNode, scope : Scope):
        if self.show:print("Visited OrNode")
        return self.visit(node.left, scope.create_child()) or self.visit(node.right, scope.create_child())
    
    @visitor.when(AndNode)
    def visit(self, node : AndNode, scope : Scope):
        if self.show:print("Visited AndNode")
        return self.visit(node.left, scope.create_child()) or self.visit(node.right, scope.create_child())
    
    @visitor.when(NotNode)
    def visit(self, node : NotNode, scope : Scope):
        if self.show:print("Visited NotNode")
        return not(self.visit(node.node, scope))
    
    @visitor.when(ComparerNode)
    def visit(self, node : ComparerNode, scope : Scope):
        if self.show:print("Visited ComparerNode")
        match node.operator:
            case '<=':
                return self.visit(node.left, scope.create_child()) <= self.visit(node.right, scope.create_child())
            case '<':
                return self.visit(node.left, scope.create_child()) < self.visit(node.right, scope.create_child())
            case '>=':
                return self.visit(node.left, scope.create_child()) >= self.visit(node.right, scope.create_child())
            case '>':
                return self.visit(node.left, scope.create_child()) > self.visit(node.right, scope.create_child())
            case '==':
                return self.visit(node.left, scope.create_child()) == self.visit(node.right, scope.create_child())
            case '!=':
                return self.visit(node.left, scope.create_child()) != self.visit(node.right, scope.create_child())
    
    @visitor.when(ArithmeticNode)
    def visit(self, node : ArithmeticNode, scope : Scope):
        if self.show:print("Visited ArithmeticNode")
        match node.operator:
            case '+':
                return self.visit(node.left, scope.create_child()) + self.visit(node.right, scope.create_child())
            case '-':
                return self.visit(node.left, scope.create_child()) - self.visit(node.right, scope.create_child())
            case '*':
                return self.visit(node.left, scope.create_child()) * self.visit(node.right, scope.create_child())
            case '/':
                try:
                    return self.visit(node.left, scope.create_child()) / self.visit(node.right, scope.create_child())
                except:
                    raise Exception("ERROR Line " + str(node.line) + ": Division by zero is not allowed")
            case '%':
                return self.visit(node.left, scope.create_child()) % self.visit(node.right, scope.create_child())
            case '**':
                return self.visit(node.left, scope.create_child()) ** self.visit(node.right, scope.create_child())
            case '^':
                return self.visit(node.left, scope.create_child()) ** self.visit(node.right, scope.create_child())
    
    @visitor.when(ConcatNode)
    def visit(self, node : ConcatNode, scope : Scope):
        if self.show:print("Visited ConcatNode")
        return_value = self.visit(node.left, scope.create_child())
        if not isinstance (return_value, str):
            return_value = str(return_value)
        #Yes, we are savages!!
        for i in range(1, len(node.operator)):
            return_value = return_value + " "
        suffix = self.visit(node.right, scope.create_child())
        if not isinstance(suffix, str):
            suffix = str(suffix)
        return_value = return_value + suffix
        return return_value
    
    @visitor.when(PredefinedFunctionNode)
    def visit(self, node : PredefinedFunctionNode, scope : Scope):
        if self.show:print("Visited PredefinedFunctionNode")
        if node.lex == 'rand':
            return random()
        value = scope.find_variable('value').value
        match node.lex:
            case 'print':
                print(value)
                return None
            case 'sin':
                return math.sin(value)
            case 'cos':
                return math.cos(value)
            case 'log':
                try:
                    base = value
                    value = scope.find_variable('base').value
                    return math.log(value, base)
                except:
                    return math.log(value)
            case 'sqrt':
                return math.sqrt(value)
            case 'exp':
                return math.exp(value)
    
    @visitor.when(IsNode)
    def visit(self, node : IsNode, scope : Scope):
        if self.show:print("Visited IsNode")
        value = self.visit(node.left, scope)
        match node.right.lex:
            case 'Number':
                return isinstance(value, float) or isinstance(value, int)
            case 'Boolean':
                return isinstance(value, bool)
            case 'Literal':
                return isinstance(value, str)
        right_type = self.context.get_type(node.right.lex)
        return value.type.conforms_to(right_type)
    
    @visitor.when(AsNode)
    def visit(self, node : AsNode, scope : Scope):
        if self.show:print("Visited AsNode")
        value = self.visit(node.left, scope)
        match node.right.lex:
            case 'Number':
                if (isinstance(value, float) or isinstance(value, int)):
                    return value
                else:
                    raise Exception(WRONG_DOWNCASTING%(node.line, "bla", 'Number'))
            case 'Boolean':
                if isinstance(value, bool):
                    return value
                else:
                    raise Exception(WRONG_DOWNCASTING%(node.line, "bla", 'Boolean'))
            case 'Literal':
                if isinstance(value, str):
                    return value
                else:
                    raise Exception(WRONG_DOWNCASTING%(node.line, "bla", 'Literal'))
        right_type = self.context.get_type(node.right.lex)
        if value.type.conforms_to(right_type):
            value.type = right_type
            return value
        else:
            raise Exception(WRONG_DOWNCASTING%(node.line, "bla", right_type))