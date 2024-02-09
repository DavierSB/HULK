def is_alpha(c): return c.isalpha()
def is_alpha_or_digit_or__(c): return c.isalpha() or c.isdigit() or c == '_'
def is_digit(c): return c.isdigit()
def is_opened_parenthesis(c): return c == '('
def is_closed_parenthesis(c): return c == ')'
def is_opened_bracket(c): return c == '['
def is_closed_bracket(c): return c == ']'
def is_opened_brace(c): return c == '{'
def is_closed_brace(c): return c == '}'
def is_plus(c): return c == '+'
def is_minus(c): return c == '-'
def is_asterisk(c): return c == '*'
def is_slash(c): return c == '/'
def is_caret(c): return c == '^'
def is_arroba(c): return c == '@'
def is_mod(c): return c == '%'
def is_pipe(c): return c == '|'
def is_ampersand(c): return c == '&'
def is_equal(c): return c == '='
def is_less_than(c): return c == '<'
def is_greater_than(c): return c == '>'
def is_colon(c): return c == ':'
def is_semicolon(c): return c == ';'
def is_comma(c): return c == ','
def is_dot(c): return c == '.'
def is_e(c): return c == 'e'
def is_ignore(c): return c == '\n' or c == '\t' or c == ' '
def is_newline(c): return c == '\n'
def is_backslash(c): return c == '\\'
def is_not_backslash(c): return not is_backslash(c)
def is_not_backslash_or_quote(c): return not is_backslash(c) and not is_quote(c)
def is_not_newline(c): return c != '\n'
def is_everything(c): return True
def is_quote(c): return c == '"'
