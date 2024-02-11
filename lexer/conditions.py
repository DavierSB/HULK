def is_equal_to(c):
    return (lambda x : (x == c))
def is_not(c):
    return (lambda x : (x != c))
def is_any_of(l : list):
    return (lambda x : x in l)
def is_none_of(l : list):
    return (lambda x : not(x in l))
def is_alpha(c): return c.isalpha()
def is_alpha_or_digit_or__(c): return c.isalpha() or c.isdigit() or c == '_'
def is_digit(c): return c.isdigit()
def is_anything(c): return True