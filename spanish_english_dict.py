import atexit
import pickle
import requests

_DICTFILE = '.glosbedict.p'

global _cache
try:
    with open(_DICTFILE, 'rb') as infile:
        _cache = pickle.load(infile)
except EnvironmentError:
    _cache = dict()

def _save_cache_exit_handler():
    with open(_DICTFILE, 'wb') as outfile:
        pickle.dump(_cache, outfile)

atexit.register(_save_cache_exit_handler)

_keep_chars = [
    'a', 'e', 'o', 'n', 's', 'r', 'i', 'l', 'd', 'u', 'c', 't', 'm', '́', 'p',
    'b', 'q', 'v', 'g', 'h', 'y', 'f', 'j', 'z', '̃', 'x', '̈', 'w', 'k', 'í',
    'ó', 'á', 'é', 'ñ', 'ú', 'ü']
def _clean_word(word):
    return ''.join(l for l in word.lower() if l in _keep_chars)

def word_info(word):
    'Get information on a word from GlosbeAPI.'
    global _cache
    word = _clean_word(word)
    if word in _cache:
        return _cache[word]
    payload = {'from': 'spa', 'dest': 'eng', 'format': 'json', 'phrase': word}
    r = requests.get('https://glosbe.com/gapi/translate', params=payload)
    if r.status_code != 200:
        return None
    _cache[word] = r.json()
    return _cache[word]
