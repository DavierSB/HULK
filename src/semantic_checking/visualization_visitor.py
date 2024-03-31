import os
import sys
current_dir = os.getcwd()
sys.path.insert(0, current_dir + '/src')
sys.path.insert(0, current_dir + 'src/semantic_checking')
import cmp.visitor as visitor
from semantic_checking.AST import *

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        expression = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{statements}\n{expression}'

    @visitor.when(ConstantValueNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'\\__' + node.name_of_node() + ' : ' + node.lex
    
    @visitor.when(SelfNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'\\__' + node.name_of_node()

    @visitor.when(BinaryExpression)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(NotNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        node = self.visit(node.node, tabs + 1)
        return f'{ans}\n{node}'
    
    @visitor.when(GenericBinaryOperationBetweenExpressions)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node() + ' ' + node.operator
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        name = self.visit(node.name, tabs + 1)
        arguments = '\n'.join(self.visit(child, tabs + 1) for child in node.arguments)
        return f'{ans}\n{name}\n{arguments}'

    @visitor.when(DeclarationNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        id = self.visit(node.id, tabs + 1)
        type_annotation = self.visit(node.type_annotation, tabs + 1)
        expression = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{id}\n{type_annotation}\n{expression}'
    
    @visitor.when(LetNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        declarations = '\n'.join(self.visit(child, tabs + 1) for child in node.declarations)
        expression = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{declarations}\n{expression}'
    
    @visitor.when(IfNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        conditions = '\t' * (tabs+1) + 'Conditions\n' + '\n'.join(self.visit(child, tabs + 1) for child in node.conditions)
        expressions = '\t' * (tabs+1) + 'Expressions\n' + '\n'.join(self.visit(child, tabs + 1) for child in node.expressions)
        else_case = '\t' * (tabs+1) + 'Else Case\n' + self.visit(node.else_case, tabs + 1)
        return f'{ans}\n{conditions}\n{expressions}\n{else_case}'
    
    @visitor.when(WhileNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        condition = '\t' * (tabs+1) + 'Condition\n' + self.visit(node.condition, tabs + 1)
        expression = '\t' * (tabs+1) + 'Expression\n' + self.visit(node.expression, tabs + 1)
        return f'{ans}\n{condition}\n{expression}'
    
    @visitor.when(ForNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        variable_id = self.visit(node.variable_id, tabs + 1)
        type_annotation = self.visit(node.type_annotation, tabs + 1)
        iterable = '\t' * (tabs+1) + 'Iterable\n' + self.visit(node.iterable, tabs + 1)
        expression = '\t' * (tabs+1) + 'Expressions\n' + self.visit(node.expression, tabs + 1)
        return f'{ans}\n{variable_id}\n{type_annotation}\n{iterable}\n{expression}'
    
    @visitor.when(NewNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        type_name = self.visit(node.type_name, tabs + 1)
        arguments = '\n'.join(self.visit(child, tabs + 1) for child in node.arguments)
        return f'{ans}\n{type_name}\n{arguments}'
    
    @visitor.when(ExpressionBlockNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        expressions = '\n'.join(self.visit(child, tabs + 1) for child in node.expressions)
        return f'{ans}\n{expressions}'
    
    @visitor.when(ParameterNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        id = self.visit(node.id, tabs + 1)
        type_annotation = self.visit(node.type_annotation, tabs + 1)
        return f'{ans}\n{id}\n{type_annotation}'
    
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        name = self.visit(node.name, tabs + 1)
        if len(node.parameters) > 0:
            parameters = '\t' * (tabs+1) + 'Parameters\n' + '\n'.join(self.visit(child, tabs + 1) for child in node.parameters)
        else:
            parameters = '\t' * (tabs+1) + 'No Parameters'
        type_annotation = self.visit(node.type_annotation, tabs + 1)
        expression = '\t' * (tabs+1) + 'Body\n' + self.visit(node.expression, tabs + 1)
        return f'{ans}\n{name}\n{type_annotation}\n{parameters}\n{expression}'

    @visitor.when(TypeDefinitionNode)
    def visit(self, node : TypeDefinitionNode, tabs = 0):
        ans = '\t' * tabs + f'\\__' + node.name_of_node()
        name = self.visit(node.name, tabs + 1)
        if len(node.own_parameters) > 0:
            own_parameters = '\t' * (tabs+1) + 'Parameters\n' + '\n'.join(self.visit(child, tabs + 1) for child in node.own_parameters)
        else:
            own_parameters = '\t' * (tabs+1) + 'No Parameters'
        if node.parent_name:
            parent_name = '\t' * (tabs+1) + 'Parent Name\n' + self.visit(node.parent_name, tabs + 1)
            parent_arguments = '\n' + '\t' * (tabs+1) + 'Parent Arguments\n' + '\n'.join(self.visit(child, tabs + 1) for child in node.parent_arguments)
        else:
            parent_name = '\t' * (tabs+1) + 'No Inheritance'
            parent_arguments = ''
        if len(node.attribute_declarations):
            attribute_declarations = '\t' * (tabs+1) + 'Attribute Declarations\n' + '\n'.join(self.visit(child, tabs + 1) for child in node.attribute_declarations)
        else:
            attribute_declarations = 'No Atributte Declaration'
        if len(node.function_declarations):
            function_declarations = '\t' * (tabs+1) + 'Function Declarations\n' + '\n'.join(self.visit(child, tabs + 1) for child in node.function_declarations)
        else:
            function_declarations = 'No Function Declaration'
        return f'{ans}\n{name}\n{own_parameters}\n{parent_name + parent_arguments}\n{attribute_declarations}\n{function_declarations}'