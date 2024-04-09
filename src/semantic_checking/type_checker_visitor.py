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
ATTRIBUTES_ARE_PRIVATE = 'Attributes are always private'
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
        self.base_method : Method = None
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
        
        #Verifiquemos que se pasen los argumentos correctos al constructor del padre
        if node.parent_name:
            received_parent_arguments = []
            for argument in node.parent_arguments:
                received_parent_arguments.append(self.visit(argument, scope_for_attribute_declarations))
            try:
                parent : Type = self.context.get_type(node.parent_name.lex)
                parent_constructor : Method = parent.get_method('__constructor__')
                for i in range(len(received_parent_arguments)):
                    if not received_parent_arguments[i].conforms_to(parent_constructor.param_types[i]):
                        self.errors.append((node.line, INCOMPATIBLE_TYPES%(received_parent_arguments[i], parent_constructor.param_types[i])))
            except:
                #LLegamos aqui solo en los casos en los que el padre es un tipo que no ha sido
                #definido. Este error debio ser reportado en el TypeBuilder. Por tanto, PASS
                pass

        for attribute_declaration in node.attribute_declarations:
            attribute = self.current_type.get_attribute(attribute_declaration.id.lex)
            inferred_type = self.visit(attribute_declaration, scope_for_attribute_declarations)
            if not inferred_type.conforms_to(attribute.type):
                self.errors.append((node.line, INCOMPATIBLE_TYPES%(inferred_type, attribute.type)))
            else:
                attribute.type = inferred_type
        for function_declaration in node.function_declarations:
            method = self.current_type.get_method(function_declaration.name.lex)
            inferred_type = self.visit(function_declaration, scope, node)
            if not inferred_type.conforms_to(method.return_type):
                self.errors.append((node.line, INCOMPATIBLE_TYPES%(inferred_type, method.return_type)))
            else:
                method.return_type = inferred_type
        self.current_type = None
    
    @visitor.when(DeclarationNode)
    def visit(self, node : DeclarationNode, scope : Scope, args : bool = False):
        print("Visited Declaration Node")
        inside_a_let = args
        var_name = node.id.lex
        if scope.is_local(var_name):
            if inside_a_let:
                self.errors.append((node.line, LET_VARIABLE_ALREADY_DEFINED%(var_name, self.current_method.name)))
        if inside_a_let:
            var_expected_type = self.context.get_type(node.type_annotation.lex)
        else:
            #Las declaraciones ocurren adentro de un let, o de la declaracion de un tipo
            var_expected_type = self.current_type.get_attribute(var_name).type
        var_inferred_type = self.visit(node.expression, scope.create_child())
        if not var_inferred_type.conforms_to(var_expected_type):
            self.errors.append((node.line, INCOMPATIBLE_TYPES%(var_inferred_type.name, var_expected_type.name)))
        if inside_a_let:
            scope.define_variable(var_name, var_inferred_type)
        node.inferred_type = var_inferred_type
        return var_inferred_type
    
    @visitor.when(ReassignNode)
    def visit(self, node : ReassignNode, scope : Scope, args = None):
        print("Visited Reassign Node")
        #SOLO ACEPTO REASIGNACIONES QUE MANTENGAN EL TIPO ORIGINAL DE LA VARIABLE
        if isinstance(node.left, MemberNode):
            if isinstance(node.left.right, FunctionCallNode):
                self.errors.append((node.line, "Functions cannot be redefined"))
                return ErrorType()
            attribute_type = self.visit(node.left, scope.create_child())
            inferred_type = self.visit(node.right, scope.create_child())
            if not inferred_type.conforms_to(attribute_type):
                self.errors.append((node.line, INCOMPATIBLE_TYPES%(inferred_type.name, attribute_type.name)))
            node.inferred_type = inferred_type
            return inferred_type
        if isinstance(node.left, IDNode):
            var_name = node.left.lex
            if not scope.is_defined(var_name):
                self.errors.append((node.line, VARIABLE_NOT_DEFINED%(var_name)))
            var_type = scope.find_variable(var_name).type
            inferred_type = self.visit(node.right, scope.create_child())
            if not inferred_type.conforms_to(var_type):
                self.errors.append((node.line, INCOMPATIBLE_TYPES%(inferred_type.name, var_type.name)))
            node.inferred_type = inferred_type
            return inferred_type
        self.errors.append((node.line, "Can only reassign variables or attributes"))
        return ErrorType()
    
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node : FunctionDefinitionNode, scope : Scope, args = None):
        print("Visited Function Definition Node")
        self.currently_inside_a_function = True
        func_expected_type = self.context.get_type(node.type_annotation.lex)
        body_scope = scope.create_child()
        previous_base_method = self.base_method
        if self.current_type:
            body_scope.define_variable('self', self.current_type)
            if self.current_type.parent:
                try:
                    self.base_method : Method = self.current_type.parent.get_method(node.name.lex)
                except:
                    pass
        for parameter_node in node.parameters:
            var_name = parameter_node.id.lex
            var_type = self.context.get_type(parameter_node.type_annotation.lex)
            body_scope.define_variable(var_name, var_type)
        func_inferred_type = self.visit(node.expression, body_scope)
        if not func_inferred_type.conforms_to(func_expected_type):
            self.errors.append((node.line, INCOMPATIBLE_TYPES%(func_inferred_type.name, func_expected_type.name)))
        self.currently_inside_a_function = False
        self.base_method = previous_base_method
        return func_inferred_type

    #Expressions
    @visitor.when(ExpressionBlockNode)
    def visit(self, node : ExpressionBlockNode, scope : Scope, args = None):
        print("Visited Block Expression Node")
        return_type = VoidType()
        for expression in node.expressions:
            return_type = self.visit(expression, scope)
        node.inferred_type = return_type
        return return_type
    
    @visitor.when(LetNode)
    def visit(self, node : LetNode, scope : Scope, args = None):
        print("Visited Let Node")
        body_scope = scope.create_child()
        for declaration in node.declarations:
            self.visit(declaration, body_scope, True)
        node.inferred_type = self.visit(node.expression, body_scope)
        return node.inferred_type

    @visitor.when(IfNode)
    def visit(self, node : IfNode, scope : Scope, args = None):
        print("Visited If Node")
        boolean_type = self.context.get_type('Boolean')
        for condition in node.conditions:
            condition_type = self.visit(condition, scope.create_child())
            if not condition_type.conforms_to(boolean_type):
                self.errors.append((node.line, INCOMPATIBLE_TYPES%(condition_type.name, boolean_type.name)))
        inferred_type = None
        for expression in (node.expressions + [node.else_case]):
            particular_return_type = self.visit(expression, scope.create_child())
            if not inferred_type:
                inferred_type = particular_return_type
            else:
                if (inferred_type == particular_return_type):
                    continue
                inferred_type = self.context.lowest_common_ancestor(inferred_type, particular_return_type)
        node.inferred_type = inferred_type
        return node.inferred_type
    
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
            self.errors.append((node.line, INCOMPATIBLE_TYPES%(condition_type.name, boolean_type.name)))
        node.inferred_type = self.visit(node.expression, scope.create_child())
        return node.inferred_type
    
    @visitor.when(NewNode)
    def visit(self, node : NewNode, scope : Scope, args = None):
        print("Visited New Node")
        received_arguments_types : List[Type] = []
        for argument in node.arguments:
            received_arguments_types.append(self.visit(argument, scope.create_child()))
        try:
            type_to_instantiate : Type = self.context.get_type(node.type_name.lex)
            constructor : Method = type_to_instantiate.get_method('__constructor__')
            for i in range(len(received_arguments_types)):
                if not received_arguments_types[i].conforms_to(constructor.param_types[i]):
                    self.errors.append((node.line, INCOMPATIBLE_TYPES%(received_arguments_types[i], constructor.param_types[i])))
            node.inferred_type = type_to_instantiate
            return type_to_instantiate
        except Exception as ex:
            try:
                self.errors.append((node.line, ex.text))
            except:
                pass
            return ErrorType()
    
    @visitor.when(MemberNode)
    def visit(self, node : MemberNode, scope : Scope, args = None):
        print("Visited Member Node")
        if isinstance(node.left, SelfNode):
            if not self.currently_inside_a_function:
                self.errors.append((node.line, SELF_ACCESOR_OUT_OF_A_FUNCTION))
        left_side_type : Type = self.visit(node.left, scope.create_child())
        if isinstance(node.right, FunctionCallNode):
            try:
                function_name = node.right.name.lex
                function_called : Method = left_side_type.get_method(function_name)
                previous_current_type = self.current_type
                self.current_type = left_side_type
                inferred_type =  self.visit(node.right, scope.create_child(), function_called)
                self.current_type = previous_current_type
                node.inferred_type = inferred_type
                return inferred_type
            except:
                self.errors.append((node.line, FUNCTION_NOT_DEFINED_IN_TYPE%(left_side_type.name, function_name)))
                return ErrorType()
        if isinstance(node.right, IDNode):
            if isinstance(node.left, SelfNode):
                try:
                    attribute_name = node.right.lex
                    attribute : Attribute = left_side_type.get_attribute(attribute_name)
                    node.inferred_type = attribute.type
                    return attribute.type
                except:
                    self.errors.append((node.line, ATTRIBUTE_NOT_DEFINED%(left_side_type.name, attribute_name)))
                    return ErrorType()
            else:
                self.errors.append((node.line, ATTRIBUTES_ARE_PRIVATE))
                return ErrorType()
        self.errors.append((node.line, BAD_MEMBER))
    
    #Constant Values
    @visitor.when(IDNode)
    def visit(self, node : IDNode, scope : Scope, args = None):
        print("Visited ID Node")
        try:
            type = scope.find_variable(node.lex).type
            node.inferred_type = type
            return type
        except:
            self.errors.append((node.line, VARIABLE_NOT_DEFINED%(node.lex)))
            return ErrorType()
    
    @visitor.when(SelfNode)
    def visit(self, node : SelfNode, scope : Scope, args = None):
        print("Visited Self Node")
        node.inferred_type  = self.current_type
        return self.current_type
    
    @visitor.when(NumberNode)
    def visit(self, node : NumberNode, scope : Scope, args = None):
        print("Visited Number Node")
        number_type = self.context.get_type('Number')
        node.inferred_type = number_type
        return number_type
    
    @visitor.when(LiteralNode)
    def visit(self, node : LiteralNode, scope : Scope, args = None):
        print("Visited Literal Node")
        literal_type = self.context.get_type('Literal')
        node.inferred_type = literal_type
        return literal_type
    
    @visitor.when(BooleanNode)
    def visit(self, node : BooleanNode, scope : Scope, args = None):
        print("Visited Boolean Node")
        boolean_type = self.context.get_type('Boolean')
        node.inferred_type = boolean_type
        return boolean_type
    
    @visitor.when(FunctionCallNode)
    def visit(self, node : FunctionCallNode, scope : Scope, args : Method = None):
        print("Visit FunctionCallNode")
        method = args #Si es None, quiere decir que la funcion que llaman es global
        received_arguments_types : List[Type] = []
        previous_base_method = self.base_method
        for argument in node.arguments:
            received_arguments_types.append(self.visit(argument, scope.create_child()))

        if method is None:
            if node.name.lex == "base":
                method = self.base_method
                if method is None:
                    method = node.base_method
                else:
                    node.base_method = self.base_method
                    try:
                        self.base_method = self.current_type.parent.base_method
                    except:
                        self.base_method = None
                    #Esto no es mas que un parche, porque el problema real es que se visite dos veces este nodo,
                    #eso ta flojo

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
            input()
            self.errors.append((node.line, FUNCTION_NOT_DEFINED_GLOBALLY%(node.name.lex)))
            return ErrorType()
        
        for i in range(len(received_arguments_types)):
            if not received_arguments_types[i].conforms_to(method.param_types[i]):
                self.errors.append((node.line, INCOMPATIBLE_TYPES%(received_arguments_types[i], method.param_types[i])))
            else:
                scope.define_variable(method.param_names[i], method.param_types[i])
        
        previous_currently_inside_a_function = self.currently_inside_a_function
        self.currently_inside_a_function = True
        inferred_type = self.visit(method.expression, scope.create_child())
        self.currently_inside_a_function = previous_currently_inside_a_function
        self.base_method = previous_base_method
        if not inferred_type.conforms_to(method.return_type):
            self.errors.append((node.line, INCOMPATIBLE_TYPES%(inferred_type, method.return_type)))
            return ErrorType()
        node.method = method
        node.inferred_type = inferred_type
        return inferred_type #Ojo con esto

    #Operations
    @visitor.when(OrNode)
    def visit(self, node : OrNode, scope : Scope, args = None):
        print("Visited Or Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        boolean_type = self.context.get_type('Boolean')
        if not(left_inferred_type.conforms_to(boolean_type) and right_inferred_type.conforms_to(boolean_type)):
            self.errors.append((node.line, INVALID_OPERATION%('Or', left_inferred_type.name, right_inferred_type.name)))
        node.inferred_type = boolean_type
        return boolean_type
    
    @visitor.when(AndNode)
    def visit(self, node : AndNode, scope : Scope, args = None):
        print("Visited And Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        boolean_type = self.context.get_type('Boolean')
        if not(left_inferred_type.conforms_to(boolean_type) and right_inferred_type.conforms_to(boolean_type)):
            self.errors.append((node.line, INVALID_OPERATION%('And', left_inferred_type.name, right_inferred_type.name)))
        node.inferred_type = boolean_type
        return boolean_type
    
    @visitor.when(NotNode)
    def visit(self, node : NotNode, scope : Scope, args = None):
        print("Visited Not Node")
        node_inferred_type : Type = self.visit(node.node, scope.create_child())
        boolean_type = self.context.get_type('Boolean')
        if not(node_inferred_type.conforms_to(boolean_type)):
            self.errors.append((node.line, INVALID_OPERATION%('Not', node_inferred_type.name)))
        boolean_type = self.context.get_type('Boolean')
        node.inferred_type = self.context.get_type('Boolean')
        return boolean_type
    
    @visitor.when(ComparerNode)
    def visit(self, node : ComparerNode, scope : Scope, args = None):
        print("Visited Comparer Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        boolean_type = self.context.get_type('Boolean')
        number_type = self.context.get_type('Number')
        if node.operator in [">", ">=", "<", "<="]:
            if not(left_inferred_type.conforms_to(number_type) and right_inferred_type.conforms_to(number_type)):
                self.errors.append((node.line, INVALID_OPERATION%(node.operator, left_inferred_type.name, right_inferred_type.name)))
        node.inferred_type = boolean_type
        return boolean_type
    
    @visitor.when(ArithmeticNode)
    def visit(self, node : ArithmeticNode, scope : Scope, args = None):
        print("Visited Arithmetic Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        number_type = self.context.get_type('Number')
        if not(left_inferred_type.conforms_to(number_type) and right_inferred_type.conforms_to(number_type)):
            self.errors.append((node.line, INVALID_OPERATION%(node.operator, left_inferred_type.name, right_inferred_type.name)))
        node.inferred_type = number_type
        return number_type
    
    @visitor.when(ConcatNode)
    def visit(self, node : ConcatNode, scope : Scope, args = None):
        print("Visited Concat Node")
        left_inferred_type : Type = self.visit(node.left, scope.create_child())
        right_inferred_type : Type = self.visit(node.right, scope.create_child())
        literal_type = self.context.get_type('Literal')
        constant_type = self.context.get_type('Constant')
        if (not (left_inferred_type.conforms_to(constant_type))) or (not (right_inferred_type.conforms_to(constant_type))):
            self.errors.append((node.line, INVALID_OPERATION%(node.operator, left_inferred_type.name, right_inferred_type.name)))
        node.inferred_type = literal_type
        return literal_type
    
    @visitor.when(IsNode)
    def visit(self, node : IsNode, scope : Scope, args = None):
        print("Visited Is Node")
        self.visit(node.left, scope.create_child())
        boolean_type = self.context.get_type('Boolean')
        node.inferred_type = boolean_type
        return boolean_type
    
    @visitor.when(AsNode)
    def visit(self, node : AsNode, scope : Scope, args = None):
        print("Visited As Node")
        return_type = self.context.get_type(node.right.lex)
        node.inferred_type = return_type
        return return_type
    
    @visitor.when(PredefinedFunctionNode)
    def visit(self, node : PredefinedFunctionNode, scope : Scope, args = Node):
        if node.lex == 'print':
            return VoidType()
        return self.context.get_type('Number')