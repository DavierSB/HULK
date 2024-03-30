scripts = [
    '42;',#0
    'let a = 0 in 42;',#1
    'function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);42;',#2
    """type Knight inherits Person {
    name() => "Sir" @@ base();
    }
    for (x in range(0, 10)) print(x);
    """#3
]

codes_for_benchmark = ["""print(ast)
print(ast.statements)
print(ast.expression)
func_decl = ast.statements[0]
print(func_decl.name)
print(func_decl.parameters)
print(func_decl.type_annotation)
print(func_decl.expression)
if_ = func_decl.expression
print(if_.conditions)
print(if_.expressions)
print(if_.else_case)
or_ = if_.conditions[0]
print(or_.left)
print(or_.right)
comparer_ = or_.right
print(comparer_.left)
print(comparer_.right)
print(comparer_.operator)""", #2
"""print(ast)
print(ast.statements)
print(ast.expression)
for_ = ast.expression
print(for_.variable_id)
print(for_.type_annotation)
print(for_.iterable)
print(for_.expression)
range_call = for_.iterable
print(range_call.left)
print(range_call.right)
type_ = ast.statements[0]
print(type_.name)
print(type_.own_parameters)
print(type_.parent_name)
print(type_.parent_arguments)
print(type_.expression)
func_decl = type_.expression[1][0]
print(func_decl.name)
print(func_decl.parameters)
print(func_decl.type_annotation)
print(func_decl.expression)
"""
]