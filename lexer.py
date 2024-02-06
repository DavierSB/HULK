
class expression_form:
    def __init__(self, args) -> None:
        self.start_form = ""
        self.show_start = True
        self.rest_form = ""
        self.show_rest = True
        self.end_form = ""
        self.show_end = True
        self.rest_unique_form = ""
        i = 0
        if args[i] == '~':
            self.show_start = False
            i=i+1
        if args[i] == '[':
            i=i+1
            while args[i] != ']':
                self.start_form = self.start_form + args[i]
                i=i+1
            i=i+1
        if args[i] == '~':
            self.show_rest = False
            i=i+1
        if args[i] == '[':
            i=i+1
            while args[i] != ']':
                self.rest_form = self.rest_form + args[i]
                i=i+1
            i=i+1
        if args[i] == '~':
            self.show_end = False
            i=i+1
        if args[i] == '[':
            i=i+1
            while args[i] != ']':
                self.end_form = self.end_form + args[i]
                i=i+1
            i=i+1
        if args[i] == '~':
            self.show_unique = False
            i=i+1
        if args[i] == '[':
            i=i+1
            while args[i] != ']':
                self.rest_unique_form = self.rest_unique_form + args[i]
                i=i+1
            i=i+1  

num = expression_form('[0123456789-][0123456789][][.e]')
id = expression_form('[abcdefghijklmnoprstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ][abcdefghijklmnoprstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ_][][]')
literal = expression_form('~["][*]~["][]')
ignore_line = expression_form('~[#]~[*]~[\n][]')
ignore_element = expression_form('~[\t\n ][][][]')
valid_expressions = [num, id, literal, ignore_line, ignore_element]
predefined_symbols = ["@", "+", "-", "*", "/", "^", "=", ":=", "==", "<", "<=", ">", ">=", "(", ")", "{", "}", "[", "]", ";"]



def is_prefix(prefix, world):
    if len(prefix) > len(world): return False
    for i in range(len(prefix)):
        if prefix[i] != world[i]:
            return False
    return True

def analyse_predefined_symbols(args, i):
    predefined_possible_symbols = predefined_symbols.copy()
    act = "" + args[i]; aux = None
    while len(predefined_possible_symbols) > 1:
        t = len(predefined_possible_symbols)
        k=0
        for j in range(t):
            if act == predefined_possible_symbols[j-k]: aux = predefined_possible_symbols[j-k]
            if not is_prefix(act, predefined_possible_symbols[j-k]):
                predefined_possible_symbols.remove(predefined_possible_symbols[j-k])
                k=k+1
        i=i+1
        if (i ==len(args)): break
        act = act + args[i]
        
    return aux, i

def match_start(expr: expression_form, args, i, flag):
    token = ""
    if expr.start_form.count(args[i]) > 0:
        if expr.rest_unique_form.count(args[i]) != 0:
            flag = False
        if expr.show_start: token = args[i]
        i=i+1
        if i == len(args):
            if len(expr.end_form) > 0:
                return None, i, flag
    else: return None, i, flag
    return token, i, flag

def match_rest(expr: expression_form, args, i, flag):
    token = ""
    if expr.rest_form != '*':
        if i == len(args):
            return token, i, flag
        while expr.rest_form.count(args[i]) != 0 or (expr.rest_unique_form.count(args[i]) != 0 and flag):
            if expr.show_rest: token = token + args[i]
            i=i+1
            if i == len(args): 
                if len(expr.end_form) > 0:
                    return '*undefined', i, flag
                else: return token, i, flag
        return token, i, flag
    else: 
        while expr.end_form.count(args[i]) == 0:
            if args[i] == '\\' and i+1 != len(args):
                token = token + args[i+1]
                i=i+1
            elif expr.show_rest: token = token + args[i]
            i=i+1
            if i == len(args):
                if len(expr.end_form) > 0:
                    return '*undefined', i, flag
                else: return token, i, flag
        return token, i, flag

def match_end(expr: expression_form, args, i):
    if len(expr.end_form) == 0: return '', i
    elif expr.end_form.count(args[i]) != 0:
        if expr.show_end:
            return args[i], i+1
        else: return '', i+1
    else: return '*undefined', i+1

def match(expr: expression_form, args, i):
    token = None
    flag = True
    token, i, flag = match_start(expr, args, i, flag)
    if token == None: return None, i
    aux, i,flag = match_rest(expr, args, i, flag)
    if aux == '*undefined': 
        return '*undefined', i
    token = token+aux
    aux, i = match_end(expr, args, i)
    if aux == '*undefined':
        return '*undefined', i
    token = token + aux
    return token, i

def next(args, i):
    aux = None; j = 0
    for expr in valid_expressions:
        aux, j = match(expr, args, i)
        if aux != None:
            return aux, j
    aux, j = analyse_predefined_symbols(args, i)
    if aux != None:
        return aux, j
    else: return '*undefined', i+1

def tokenize(args):
    tokens = []
    act = ""
    i = 0
    while (i < len(args)):
        act, i = next(args, i)
        if act == '': continue
        tokens.append(act)
    return tokens



stmt = input()
print(tokenize(stmt))


