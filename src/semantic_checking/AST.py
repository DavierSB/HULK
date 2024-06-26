import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.utils import Token
#from cmp.ast import Node
from typing import List, Tuple

class Node():
    def __init__(self, line = None):
        self.line = line
    def name_of_node(self):
        return type(self).__name__

class ProgramNode(Node):
    def __init__(self, statements, expression, line):
        super().__init__(line)
        self.statements = statements
        self.expression = expression

class ExpressionNode(Node):
    pass

class StatementNode(Node):
    pass

#Constant_Values
class ConstantValueNode(ExpressionNode):
    def __init__(self, lex, line):
        super().__init__(line)
        self.lex = lex

class IDNode(ConstantValueNode):
    pass

class NumberNode(ConstantValueNode):
    pass

class LiteralNode(ConstantValueNode):
    pass

class BooleanNode(ConstantValueNode):
    pass

class PredefinedFunctionNode(ConstantValueNode):
    pass

#Names
class NameNode(ConstantValueNode):
    def __init__(self, name, line):
        super().__init__(name, line)

class TypeNameNode(NameNode):
    def __init__(self, name = None, line = None):
        if name == None:
            name = 'Any'
        super().__init__(name, line)

class FunctionNameNode(NameNode):
    pass

#Boolean operations
class BinaryExpression(ExpressionNode):    
    def __init__(self, left : ExpressionNode, right : ExpressionNode, line):
        super().__init__(line)
        self.left = left
        self.right = right

class OrNode(BinaryExpression):
    pass

class AndNode(BinaryExpression):
    pass

class NotNode(ExpressionNode):
    def __init__(self, node : ExpressionNode, line):
        super().__init__(line)
        self.node = node

#Is As
class BinaryExpressionOnTyping(BinaryExpression):
    def __init__(self, left : ExpressionNode, right : TypeNameNode, line):
        super().__init__(left, right, line)
        self.left = left
        self.right = right

class IsNode(BinaryExpressionOnTyping):
    pass

class AsNode(BinaryExpressionOnTyping):
    pass

#Binary Generic Operations
class GenericBinaryOperationBetweenExpressions(ExpressionNode):
    def __init__(self, left : ExpressionNode, right : ExpressionNode, operator : str, line):
        super().__init__(line)
        self.left = left
        self.right = right
        self.operator = operator

class ComparerNode(GenericBinaryOperationBetweenExpressions):
    pass

class ConcatNode(GenericBinaryOperationBetweenExpressions):
    pass

class ArithmeticNode(GenericBinaryOperationBetweenExpressions):
    pass

class SelfNode(ExpressionNode):
    pass

class MemberNode(BinaryExpression):
    pass

class FunctionCallNode(ExpressionNode):
    def __init__(self, name : FunctionNameNode, arguments : List[ExpressionNode], line):
        super().__init__(line)
        self.name = name
        self.arguments = arguments

class DeclarationNode(Node):
    def __init__(self, id : 'IDNode', type_annotation : 'TypeNameNode', expression : ExpressionNode, line):
        super().__init__(line)
        self.id = id
        self.type_annotation = type_annotation
        self.expression = expression

class LetNode(ExpressionNode):
    def __init__(self, declarations : List['DeclarationNode'], expression : ExpressionNode, line):
        super().__init__(line)
        self.declarations = declarations
        self.expression = expression

class IfNode(ExpressionNode):
    def __init__(self, conditions : List[ExpressionNode], expressions : List[ExpressionNode], else_case : ExpressionNode, line):
        super().__init__(line)
        self.conditions = conditions
        self.expressions = expressions
        self.else_case = else_case

class WhileNode(ExpressionNode):
    def __init__(self, condition : ExpressionNode, expression : ExpressionNode, line):
        super().__init__(line)
        self.condition = condition
        self.expression = expression

class ForNode(ExpressionNode):
    def __init__(self, variable_id : IDNode, type_annotation : TypeNameNode, iterable : ExpressionNode, expression : ExpressionNode, line):
        super().__init__(line)
        self.variable_id = variable_id
        self.type_annotation = type_annotation
        self.iterable = iterable
        self.expression = expression

class NewNode(ExpressionNode):
    def __init__(self, type_name : TypeNameNode, arguments : List[ExpressionNode], line):
        super().__init__(line)
        self.type_name = type_name
        self.arguments = arguments

class ReassignNode(BinaryExpression):
    pass

class ExpressionBlockNode(ExpressionNode):
    def __init__(self, expressions : List[ExpressionNode], line):
        super().__init__(line)
        self.expressions = expressions

class ParameterNode(Node):
    def __init__(self, id : IDNode, type_annotation : TypeNameNode, line):
        super().__init__(line)
        self.id = id
        self.type_annotation = type_annotation

class FunctionDefinitionNode(StatementNode):
    def __init__(self, name : FunctionNameNode, parameters : List[ParameterNode], type_annotation : TypeNameNode, expression : ExpressionNode, line):
        super().__init__(line)
        self.name = name
        self.parameters = parameters
        self.type_annotation = type_annotation
        self.expression = expression

class TypeDefinitionNode(StatementNode):
    def __init__(self, name : TypeNameNode, own_parameters : List[ParameterNode], parent_name : TypeNameNode | None, parent_arguments : List[ExpressionNode] | None, declarations : Tuple[List[DeclarationNode], List[FunctionDefinitionNode]], line):
        super().__init__(line)
        self.name = name
        self.own_parameters = own_parameters
        self.parent_name = parent_name
        self.parent_arguments = parent_arguments
        self.attribute_declarations = declarations[0]
        self.function_declarations = declarations[1]

class VoidNode(Node):
    pass