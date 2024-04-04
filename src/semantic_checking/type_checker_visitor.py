import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
import cmp.visitor as visitor
from semantic_checking.AST import *
from cmp.semantic import Context, Scope, Method, Attribute, SemanticError, Type, ErrorType, VoidType
from typing import Set

WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
SELF_ACCESOR_OUT_OF_A_FUNCTION = 'Variable "self" can only be used inside of a function'
LET_VARIABLE_ALREADY_DEFINED = 'Variable "%s" is already defined in this let expression.'
ATTRIBUTE_ALREADY_DEFINED = 'Variable "%s" is already defined in type "%s"'
ATTRIBUTE_NOT_DEFINED = 'Type "%s" does not contains an attribute named "%s"'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined.'
FUNCTION_NOT_DEFINED_GLOBALLY = 'Function "%s" is not defined with this parameters'
INVALID_OPERATION = 'Operation "%s" is not defined between "%s" and "%s".'
FUNCTION_NOT_DEFINED_IN_TYPE = 'Type "%s" does not contains a function named "%s"'
BAD_MEMBER = 'Just functions and ids allowed as members of a class'
BAD_CONSTRUCTOR_CALL = 'Type "%s" recquires "%s" parameters for its construction, not "%s"'

class TypeCheckerVisitor:
    def __init__(self, context : Context, global_functions : Set[Method], errors):
        self.context = context
        self.global_functions = global_functions
        self.current_type : Type = None
        self.currently_inside_a_function : bool = False
        self.errors = errors

    @visitor.on('node')
    def visit(self, node : Node, scope, args = None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode, scope : Scope = None, args = None):
        print("Visited Program Node")
        if not scope:
            scope = Scope()
        for statement in node.statements:
            self.visit(statement, scope.create_child())
        self.visit(node.expression, scope.create_child())
    
    @visitor.when(TypeDefinitionNode)
    def visit(self, node : TypeDefinitionNode, scope : Scope, args = None):
        print("Visited Type Definition Node")
        self.current_type : Type = self.context.get_type(node.name.lex)
        scope_for_attribute_declarations = scope.create_child()
        constructor : Method = self.current_type.get_method('__constructor__')
        param_names = constructor.param_names
        param_types = constructor.param_types
        for i in range(len(param_names)):
            scope_for_attribute_declarations.define_variable(param_names[i], param_types[i])
        for attribute_declaration in node.attribute_declarations:
            self.visit(attribute_declaration, scope_for_attribute_declarations)
        for function_declaration in node.function_declarations:
            self.visit(function_declaration, scope, node)
        self.current_type = None
    
    @visitor.when(DeclarationNode)
    def visit(self, node : DeclarationNode, scope : Scope, args : Node = None):
        print("Visited Declaration Node")
        inside_a_let = isinstance(args, LetNode)
        var_name = node.id.lex
        if scope.is_local(var_name):
            if inside_a_let:
                self.errors.append(LET_VARIABLE_ALREADY_DEFINED%(var_name, self.current_method.name))
        if inside_a_let:
            var_expected_type = self.context.get_type(node.type_annotation.lex)
        else:
            var_expected_type = self.current_type.get_attribute(var_name).type
        var_inferred_type = self.visit(node.expression, scope.create_child())
        if not var_inferred_type.conforms_to(var_expected_type):
            self.errors.append(INCOMPATIBLE_TYPES%(var_inferred_type.name, var_expected_type.name))
        if inside_a_let:
            scope.define_variable(var_name, var_inferred_type)
        return var_inferred_type
    
    @visitor.when(ReassignNode)
    def visit(self, node : ReassignNode, scope : Scope, args = None):
        print("Visited Reassign Node")
        #SOLO ACEPTO REASIGNACIONES QUE MANTENGAN EL TIPO ORIGINAL DE LA VARIABLE
        if isinstance(node.left, MemberNode):
            if isinstance(node.left.right, FunctionCallNode):
                self.errors.append("Functions cannot be redefined")
                return ErrorType()
            attribute_type = self.visit(node.left, scope.create_child())
            inferred_type = self.visit(node.right, scope.create_child())
            if not inferred_type.conforms_to(attribute_type):
                self.errors.append(INCOMPATIBLE_TYPES%(inferred_type.name, attribute_type.name))
            return inferred_type
        if isinstance(node.left, IDNode):
            var_name = node.left.lex
            if not scope.is_defined(var_name):
                self.errors.append(VARIABLE_NOT_DEFINED%(var_name))
            var_type = scope.find_variable(var_name).type
            inferred_type = self.visit(node.right, scope.create_child())
            if not inferred_type.conforms_to(var_type):
                self.errors.append(INCOMPATIBLE_TYPES%(inferred_type.name, var_type.name))
            return inferred_type
        self.errors.append("Can only reassign variables or attributes")
        return ErrorType()
    
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node : FunctionDefinitionNode, scope : Scope, args = None):
        print("Visited Function Definition Node")
        self.currently_inside_a_function = True
        func_expected_type = self.context.get_type(node.type_annotation.lex)
        body_scope = scope.create_child()
        if self.current_type:
            body_scope.define_variable('self', self.current_type)
        for parameter_node in node.parameters:
            var_name = parameter_node.id.lex
            var_type = self.context.get_type(parameter_node.type_annotation.lex)
            body_scope.define_variable(var_name, var_type)
        func_inferred_type = self.visit(node.expression, body_scope)
        if not func_inferred_type.conforms_to(func_expected_type):
            self.errors.append(INCOMPATIBLE_TYPES%(func_inferred_type.name, func_expected_type.name))
        self.currently_inside_a_function = False

    #Expressions
    @visitor.when(ExpressionBlockNode)
    def visit(self, node : ExpressionBlockNode, scope : Scope, args = None):
        print("Visited Block Expression Node")
        return_type = VoidType()
        for expression in node.expressions:
            return_type = self.visit(expression, scope)
        return return_type
    
    @visitor.when(LetNode)
    def visit(self, node : LetNode, scope : Scope, args = None):
        print("Visited Let Node")
        body_scope = scope.create_child()
        for declaration in node.declarations:
            self.visit(declaration, body_scope, node)
        return self.visit(node.expression, body_scope)
    
    @visitor.when(IfNode)
    def visit(self, node : IfNode, scope : Scope, args = None):
        print("Visited If Node")
        boolean_type = self.context.get_type('Boolean')
        for condition in node.conditions:
            condition_type = self.visit(condition, scope.create_child())
            if not condition_type.conforms_to(boolean_type):
                self.errors.append(INCOMPATIBLE_TYPES%(condition_type.name, boolean_type.name))
        for expression in node.expressions:
            self.visit(expression, scope.create_child())
        return self.context.get_type('Object')
    
    @visitor.when(ForNode)
    def visit(self, node : ForNode, scope : Scope, args = None):
        var_name = node.variable_id.lex
        var_type = node.type_annotation.lex
        scope.define_variable(var_name, self.context.get_type(var_type))
        #Q LINDO SERIA HACER PROTOCOLOS, PERO NO SE SI ME DE TIEMPO
        #iterable_type = self.context.get_type('Iterable')
        #inferred_iterable_type = self.visit(node.iterable, scope.create_child())
        #if not inferred_iterable_type.conforms_to(iterable_type):
        #    self.errors.append(INCOMPATIBLE_TYPES%(inferred_iterable_type, iterable_type))
        #type_of_current_of_iterable = inferred_iterable_type.get_method('current').return_type
        #if not var_type.conforms_to(type_of_current_of_iterable):
        #    self.errors.append(INCOMPATIBLE_TYPES%(var_type, type_of_current_of_iterable))
        return self.visit(node.expression, scope.create_child())

    @visitor.when(WhileNode)
    def visit(self, node : WhileNode, scope : Scope, args = None):
        print("Visited While Node")
        boolean_type = self.context.get_type('Boolean')
        condition_type = self.visit(node.condition, scope.create_child())
        if not condition_type.conforms_to(boolean_type):
            self.errors.append(INCOMPATIBLE_TYPES%(condition_type.name, boolean_type.name))
        return self.visit(node.expression, scope.create_child())
    
    @visitor.when(NewNode)
    def visit(self, node : NewNode, scope : Scope, args = None):
        print("Visited New Node")
        received_arguments_types : List[Type] = []
        for argument in node.arguments:
            received_arguments_types.append(self.visit(argument, scope.create_child()))
        try:
            type_to_instantiate : Type = self.context.get_type(node.type_name.lex)
            constructor : Method = type_to_instantiate.get_method('__constructor__')
            if len(received_arguments_types) != len(constructor.param_names):
                self.errors.append(BAD_CONSTRUCTOR_CALL%(type_to_instantiate.name, str(len(constructor.param_names)), str(len(received_arguments_types))))
            for i in range(len(received_arguments_types)):
                if not received_arguments_types[i].conforms_to(constructor.param_types[i]):
                    self.errors.append(INCOMPATIBLE_TYPES%(received_arguments_types[i], constructor.param_types[i]))
            return type_to_instantiate
        except Exception as ex:
            self.errors.append(ex)
            return ErrorType()
    
    @visitor.when(MemberNode)
    def visit(self, node : MemberNode, scope : Scope, args = None):
        print("Visited Member Node")
        if isinstance(node.left, SelfNode):
            if not self.currently_inside_a_function:
                self.errors.append(SELF_ACCESOR_OUT_OF_A_FUNCTION)
        left_side_type : Type = self.visit(node.left, scope.create_child())
        if isinstance(node.right, FunctionCallNode):
            try:
                function_name = node.right.name.lex
                function_called : Method = left_side_type.get_method(function_name)
                return self.visit(node.right, scope.create_child(), function_called)
            except:
                self.errors.append(FUNCTION_NOT_DEFINED_IN_TYPE%(left_side_type.name, function_name))
                return ErrorType()
        if isinstance(node.right, IDNode):
            try:
                attribute_name = node.right.lex
                attribute : Attribute = left_side_type.get_attribute(attribute_name)
                return attribute.type
            except:
                self.errors.append(ATTRIBUTE_NOT_DEFINED%(left_side_type, attribute_name))
                return ErrorType()
        self.errors.append(BAD_MEMBER)
    
    #Constant Values
    @visitor.when(IDNode)
    def visit(self, node : IDNode, scope : Scope, args = None):
        print("Visited ID Node")
        try:
            return scope.find_variable(node.lex).type
        except:
            self.errors.append(VARIABLE_NOT_DEFINED%(node.lex))
            return ErrorType()
    
    @visitor.when(SelfNode)
    def visit(self, node : SelfNode, scope : Scope, args = None):
        print("Visited Self Node")
        return self.current_type
    
    @visitor.when(NumberNode)
    def visit(self, node : NumberNode, scope : Scope, args = None):
        print("Visited Number Node")
        return self.context.get_type('Number')
    
    @visitor.when(LiteralNode)
    def visit(self, node : LiteralNode, scope : Scope, args = None):
        print("Visited Literal Node")
        return self.context.get_type('Literal')
    
    @visitor.when(BooleanNode)
    def visit(self, node : BooleanNode, scope : Scope, args = None):
        print("Visited Boolean Node")
        return self.context.get_type('Boolean')
    
    @visitor.when(FunctionCallNode)
    def visit(self, node : FunctionCallNode, scope : Scope, args : Method = None):
        method = args #Si es None, quiere decir que la funcion que llaman es global
        received_arguments_types : List[Type] = []
        for argument in node.arguments:
            received_arguments_types.append(self.visit(argument, scope.create_child()))
        
        if method is None:
            flag = False
            for func in self.global_functions:
                if (func.name == node.name.lex) and (len(received_arguments_types) == len(func.param_types)):
                    flag = True
                    for i in range(len(received_arguments_types)):
                        if not received_arguments_types[i].conforms_to(func.param_types[i]):
                            flag = False
                            break
                if flag:
                    method = func
                    break
        if method is None: #still
            self.errors.append(FUNCTION_NOT_DEFINED_GLOBALLY%(node.name.lex))
            return ErrorType()
        
        for i in range(len(received_arguments_types)):
            if not received_arguments_types[i].conforms_to(method.param_types[i]):
                self.errors.append(INCOMPATIBLE_TYPES%(received_arguments_types[i], method.param_types[i]))
        
        return method.return_type

    #Operations
    @visitor.when(OrNode)
    def visit(self, node : OrNode, scope : Scope, args = None):
        print("Visited Or Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        boolean_type = self.context.get_type('Boolean')
        if not(left_inferred_type.conforms_to(boolean_type) and right_inferred_type.conforms_to(boolean_type)):
            self.errors.append(INVALID_OPERATION%('Or', left_inferred_type.name, right_inferred_type.name))
        return boolean_type
    
    @visitor.when(AndNode)
    def visit(self, node : AndNode, scope : Scope, args = None):
        print("Visited And Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        boolean_type = self.context.get_type('Boolean')
        if not(left_inferred_type.conforms_to(boolean_type) and right_inferred_type.conforms_to(boolean_type)):
            self.errors.append(INVALID_OPERATION%('And', left_inferred_type.name, right_inferred_type.name))
        return boolean_type
    
    @visitor.when(NotNode)
    def visit(self, node : NotNode, scope : Scope, args = None):
        print("Visited Not Node")
        node_inferred_type : Type = self.visit(node.node, scope.create_child())
        boolean_type = self.context.get_type('Boolean')
        if not(node_inferred_type.conforms_to(boolean_type)):
            self.errors.append(INVALID_OPERATION%('Not', node_inferred_type.name))
        return self.context.get_type('Boolean')
    
    @visitor.when(ComparerNode)
    def visit(self, node : ComparerNode, scope : Scope, args = None):
        print("Visited Comparer Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        boolean_type = self.context.get_type('Boolean')
        number_type = self.context.get_type('Number')
        if node.operator in [">", ">=", "<", "<="]:
            if not(left_inferred_type.conforms_to(number_type) and right_inferred_type.conforms_to(number_type)):
                self.errors.append(INVALID_OPERATION%(node.operator, left_inferred_type.name, right_inferred_type.name))
        return boolean_type
    
    @visitor.when(ArithmeticNode)
    def visit(self, node : ArithmeticNode, scope : Scope, args = None):
        print("Visited Arithmetic Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        number_type = self.context.get_type('Number')
        if not(left_inferred_type.conforms_to(number_type) and right_inferred_type.conforms_to(number_type)):
            self.errors.append(INVALID_OPERATION%(node.operator, left_inferred_type.name, right_inferred_type.name))
        return number_type
    
    @visitor.when(ConcatNode)
    def visit(self, node : ConcatNode, scope : Scope, args = None):
        print("Visited Concat Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        literal_type = self.context.get_type('Literal')
        boolean_type = self.context.get_type('Boolean')
        number_type = self.context.get_type('Number')
        if (not (left_inferred_type.name in ['Number', 'Literal', 'Boolean'])) or (not (right_inferred_type.name in ['Number', 'Literal', 'Boolean'])):
            self.errors.append(INVALID_OPERATION%(node.operator, left_inferred_type.name, right_inferred_type.name))
        return literal_type
    
    @visitor.when(IsNode)
    def visit(self, node : IsNode, scope : Scope, args = None):
        print("Visited Is Node")
        self.visit(node.left, scope.create_child())
        return self.context.get_type('Boolean')
    
    @visitor.when(AsNode)
    def visit(self, node : AsNode, scope : Scope, args = None):
        print("Visited As Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        return_type : Type = self.context.get_type(node.right.lex)
        if left_inferred_type.conforms_to(return_type):
            return return_type
        self.errors.append(INCOMPATIBLE_TYPES%(left_inferred_type, return_type))