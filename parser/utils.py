from cmp.pycompiler import Sentence
from defining_grammar import grammar
def subSentence(sentence : Sentence, start : int, end : int = None):
    if end is None:
        end = len(sentence)
    symbols = sentence[start : end]
    new_sentence = None
    for symbol in symbols:
        if not new_sentence:
            new_sentence = symbol + grammar.Epsilon
        else:
            new_sentence = new_sentence + symbol
    if not new_sentence:
        new_sentence = grammar.Epsilon + grammar.Epsilon
    return new_sentence