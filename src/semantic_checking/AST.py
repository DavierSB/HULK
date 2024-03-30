import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
from cmp.utils import Token
from typing import List, Tuple

class Node:
    pass

class ProgramNode(Node):
    def __init__(self, statements, expression):
        super().__init__()
        self.statements = statements
        self.expression = expression

class ExpressionNode(Node):
    pass

class StatementNode(Node):
     pass

#Constant_Values
class ConstantValueNode(ExpressionNode):
    def __init__(self, lex):
        super().__init__()
        self.lex = lex

class IDNode(ConstantValueNode):
    pass

class NumberNode(ConstantValueNode):
    pass

class LiteralNode(ConstantValueNode):
    pass

class BooleanNode(ConstantValueNode):
    pass

#Names
class TypeNameNode(Node):
    def __init__(self, name = None):
        super().__init__()
        self.name = name

class FunctionNameNode(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

#Boolean operations
class BinaryExpression(ExpressionNode):    
    def __init__(self, left : ExpressionNode, right : ExpressionNode):
        super().__init__()
        self.left = left
        self.right = right
class OrNode(BinaryExpression):
    pass

class AndNode(BinaryExpression):
    pass

class NotNode(ExpressionNode):
    def __init__(self, node : ExpressionNode):
        super().__init__()
        self.node = node

#Binary Generic Operations
class GenericBinaryOperationBetweenExpressions(ExpressionNode):
    def __init__(self, left : ExpressionNode, right : ExpressionNode, operator : str):
        super().__init__()
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

class FunctionCallNode(BinaryExpression):
    pass

class DeclarationNode(Node):
    def __init__(self, id : 'IDNode', type_annotation : 'TypeNameNode', expression : ExpressionNode):
        super().__init__()
        self.id = id
        self.type_annotation = type_annotation
        self.expression = expression

class LetNode(ExpressionNode):
    def __init__(self, declarations : List['DeclarationNode'], expression : ExpressionNode):
        super().__init__()
        self.declarations = declarations
        self.expression = expression

class IfNode(ExpressionNode):
    def __init__(self, conditions : List[ExpressionNode], expressions : List[ExpressionNode], else_case : ExpressionNode):
        super().__init__()
        self.conditions = conditions
        self.expressions = expressions
        self.else_case = else_case

class WhileNode(ExpressionNode):
    def __init__(self, condition : ExpressionNode, expression : ExpressionNode):
        super().__init__()
        self.condition = condition
        self.expression = expression

class ForNode(ExpressionNode):
    def __init__(self, variable_id : IDNode, type_annotation : TypeNameNode, iterable : ExpressionNode, expression : ExpressionNode):
        super().__init__()
        self.variable_id = variable_id
        self.type_annotation = type_annotation
        self.iterable = iterable
        self.expression = expression

class NewNode(ExpressionNode):
    def __init__(self, type_name : TypeNameNode, arguments : List[ExpressionNode]):
        super().__init__()
        self.arguments = arguments

class ReassignNode(BinaryExpression):
    pass

class ExpressionBlockNode(ExpressionNode):
    def __init__(self, expressions : List[ExpressionNode]):
        super().__init__()
        self.expressions = expressions

class FunctionDefinitionNode(StatementNode):
    def __init__(self, name : FunctionNameNode, parameters : List[Tuple[IDNode, TypeNameNode]], type_annotation : TypeNameNode, expression : ExpressionNode):
        super().__init__()
        self.name = name
        self.parameters = parameters
        self.type_annotation = type_annotation
        self.expression = expression

class TypeDefinitionNode(StatementNode):
    def __init__(self, name : TypeNameNode, own_parameters : List[Tuple[IDNode, TypeNameNode]], parent_name : TypeNameNode | None, parent_arguments : List[ExpressionNode] | None, expression : ExpressionNode):
        super().__init__()
        self.name = name
        self.own_parameters = own_parameters
        self.parent_name = parent_name
        self.parent_arguments = parent_arguments
        self.expression = expression