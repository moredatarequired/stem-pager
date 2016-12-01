import atexit
from collections import Counter, defaultdict
import counter_stats
from nltk.stem.snowball import SpanishStemmer
import pager
import pickle
import sys

_COUNTFILE = '.leipzig_word_counts.p'
_MANUALDICT = '.personal_stems.p'

global _word_freq
with open(_COUNTFILE, 'rb') as infile:
    _word_freq = pickle.load(infile)

global _manual_dict
try:
    with open(_MANUALDICT, 'rb') as infile:
        _manual_dict = pickle.load(infile)
except EnvironmentError:
    _manual_dict = defaultdict()

def _save_cache_exit_handler():
    with open(_MANUALDICT, 'wb') as outfile:
        pickle.dump(_manual_dict, outfile)
atexit.register(_save_cache_exit_handler)

def manual_lemma(word):
    return _manual_dict.get(word)

def add_lemma(word, lemma):
    global _manual_dict
    _manual_dict[word] = lemma

def word_matches(word):
    stem = SpanishStemmer().stem(word)
    return _word_freq[stem]

def format_group(group):
    words = ['{} ({:.2f})'.format(w, c) for w, c in group.most_common() if c > 0.005]
    words = ['{}.{}'.format(i+1, w) for i, w in enumerate(words)]
    return '[{}]'.format(', '.join(words))
