import atexit
import pickle

_LEMMA_FILE = '.lemmas.p'
_SKIP_WORDS = '.skip.p'
_EXCEPTON_FILE = '.special_forms.p'

try:
    with open(_LEMMA_FILE, 'rb') as infile:
        _lemmas = pickle.load(infile)
except EnvironmentError:
    _lemmas = set()

try:
    with open(_SKIP_WORDS, 'rb') as infile:
        _skip = pickle.load(infile)
except EnvironmentError:
    _skip = set()

try:
    with open(_EXCEPTON_FILE, 'rb') as infile:
        _special_forms = pickle.load(infile)
except EnvironmentError:
    _special_forms = dict()

def _save_cache_exit_handler():
    with open(_LEMMA_FILE, 'wb') as outfile:
        pickle.dump(_lemmas, outfile)
    with open(_SKIP_WORDS, 'wb') as outfile:
        pickle.dump(_skip, outfile)
    with open(_EXCEPTON_FILE, 'wb') as outfile:
        pickle.dump(_special_forms, outfile)
atexit.register(_save_cache_exit_handler)

def add_lemma(lemma):
    global _lemmas
    _lemmas.add(lemma)

def add_skip(word):
    global _skip
    _skip.add(word)

def add_form(lemma, inflected):
    global _special_forms
    _special_forms[inflected] = lemma

def guess_lemma(word):
    '''Use various rules to find possible lemmas.'''
    return word

def get_lemma(word):
    '''Return possible lemmas for the input word, or none if unknown.'''
    if word in _lemmas:
        return word
    if word in _special_forms:
        return _special_forms[word]
    if word in _skip:
        return '-'
    return None
