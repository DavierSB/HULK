def basic_test():
    dfa = Regex('a*(a|b)*cd | ε').automaton
    assert dfa.recognize('')
    assert dfa.recognize('cd')
    assert dfa.recognize('aaaaacd')
    assert dfa.recognize('bbbbbcd')
    assert dfa.recognize('bbabababcd')
    assert dfa.recognize('aaabbabababcd')
    
    assert not dfa.recognize('cda')
    assert not dfa.recognize('aaaaa')
    assert not dfa.recognize('bbbbb')
    assert not dfa.recognize('ababba')
    assert not dfa.recognize('cdbaba')
    assert not dfa.recognize('cababad')
    assert not dfa.recognize('bababacc')

def groups_test(dfa):
    assert dfa.recognize('7.25')

def scapes_test():
    def put_scapes(pattern):
        new_pattern = pattern.replace('K', '\\')
        return new_pattern
    dfa = Regex(put_scapes('(K*K*KK*)*')).automaton
    assert dfa.recognize('')
    assert dfa.recognize('**')
    assert dfa.recognize('****')
    assert dfa.recognize('********')
    assert dfa.recognize('**\\\\\\')
    assert dfa.recognize(put_scapes('**KKKKKK'))

    assert not dfa.recognize('***')
    assert not dfa.recognize('*****')
    assert not dfa.recognize('*******')

def numbers_test():
    dfa = Regex(tokens['NUMBER']).automaton

    assert dfa.recognize('1.23')
    assert dfa.recognize('42')
    assert dfa.recognize('0.8787')
    assert dfa.recognize('42351.00')
    
    assert not dfa.recognize('03.5')
    assert not dfa.recognize('15.226.0')

def id_test():
    dfa = Regex(tokens['ID']).automaton

    assert dfa.recognize('A')
    assert dfa.recognize('davier')
    assert dfa.recognize('dAv13R')
    assert dfa.recognize('random_variable_c4b3z0N')
    assert dfa.recognize('__070__iN')
    assert dfa.recognize('_')

    assert not dfa.recognize('0.24')
    assert not dfa.recognize('ABC,D')
    assert not dfa.recognize('')

def any_char_test():
    dfa = nfa_to_dfa(AnyCharNode('').evaluate())
    assert dfa.recognize('a')
    assert dfa.recognize('z')
    assert dfa.recognize('9')

    assert not dfa.recognize('aa')
    assert not dfa.recognize('')
    assert not dfa.recognize('9876')

def char_group_test():
    dfa = Regex('[a-f]').automaton
    assert dfa.recognize('c')
    assert dfa.recognize('a')
    assert dfa.recognize('f')
    assert not dfa.recognize('g')
    assert not dfa.recognize('h')
    assert not dfa.recognize('aa')
    dfa = Regex('[^a]').automaton
    assert not dfa.recognize('a')
    assert dfa.recognize('b')
    assert not dfa.recognize('bb')
    assert dfa.recognize('@')
    dfa = Regex('[^a-f]').automaton
    assert not dfa.recognize('c')
    assert not dfa.recognize('a')
    assert not dfa.recognize('f')
    assert dfa.recognize('g')
    assert dfa.recognize('h')
    assert not dfa.recognize('aa')
    assert not dfa.recognize('gg@')
    dfa = Regex('[^abF-Z0-3]').automaton
    assert dfa.recognize('c')
    assert dfa.recognize('z')
    assert dfa.recognize('7')
    assert dfa.recognize('A')
    assert dfa.recognize('E')
    assert not dfa.recognize('a')
    assert not dfa.recognize('b')
    assert not dfa.recognize('F')
    assert not dfa.recognize('G')
    assert not dfa.recognize('3')
    assert not dfa.recognize('0')
    assert not dfa.recognize('2')
    assert not dfa.recognize('Z')
    assert not dfa.recognize('98')
    dfa = Regex('[^]').automaton
    assert dfa.recognize('a')
    assert dfa.recognize('Z')
    assert dfa.recognize('9')
    assert not dfa.recognize('98')
    return


def literal_test():
    dfa = Regex(tokens['LITERAL']).automaton
    assert not dfa.recognize('')

#basic_test()
#scapes_test()
#numbers_test()
#id_test()
#literal_test()
#complemment_test()
#any_char_test()
char_group_test()
print("LLEGUEEEEEEEEE")

def no_quotes_or_space_test():
    dfa = Regex(not_scape_or_quotation_char).automaton
    print(not_scape_or_quotation_char)
    assert dfa.recognize('a')
    assert dfa.recognize('c')
    assert dfa.recognize('\\n')
    assert dfa.recognize(' ')
    assert dfa.recognize('!')
    assert dfa.recognize('N')
    assert dfa.recognize('#')
    assert not dfa.recognize('"')
    assert not dfa.recognize('\\')
    assert not dfa.recognize("aa")

no_quotes_or_space_test()
print("LLEGUEEEE")

print(lexer("3.14 5 0.25 13"))
print(lexer('Davier _hola    3.14   \\"Hola mundo\\"   casca9jal 9'))
print(lexer('"Hola Mundo  soy Davier"'))
print(lexer('The message is \\"Hello World\\"'))
print(lexer('"Hola Mundo  el mensaje era \\"Hello World\\" y m satisface"'))
print(lexer('"Y mas aun si sabemos \\"Hello World\\" o:"" Te amo Marian"'))
print(lexer('42;'))
print(lexer('print(42);'))
print(lexer('print((((1 + 2) ^ 3) * 4) / 5);'))
print(lexer('print("Hello World");'))
print(lexer('print("The message is \"Hello World\"");'))
print(lexer('print("The meaning of life is " @ 42);'))
print(lexer('print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));'))
print(lexer("""{
    print(42);
    print(sin(PI/2));
    print("Hello World");
}"""))