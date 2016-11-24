import atexit
import pickle
from spanish_english_dict import word_info

_DICTFILE = '.stemdict.p'

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

def _translations(word):
    info = word_info(word)
    translations = []
    if 'tuc' in info:
        for tuc in info['tuc']:
            if 'phrase' in tuc:
                translations.append(tuc['phrase']['text'])
    return translations

def _meanings(word):
    info = word_info(word)
    meanings = []
    if 'tuc' in info:
        for tuc in info['tuc']:
            if 'meanings' in tuc:
                for meaning in tuc['meanings']:
                    if meaning['language'] == 'es':
                        meanings.append(meaning['text'])
    return meanings

def replace_suffix(word, old_suffix, new_suffix):
    if word.endswith(old_suffix):
        return word[:-len(old_suffix)] + new_suffix
    return None

def core_stems(word):
    possible_stems = []
    # pronoun suffixes
    for pronoun in ('me', 'te', 'le', 'lo', 'la', 'se', 'las', 'los', 'les'):
        nw = replace_suffix(word, pronoun, '')
        if nw:
            possible_stems += stems(nw)
    # plural
    nw = replace_suffix(word, 's', '')
    if nw and not possible_stems:
        possible_stems += stems(nw)
    # congugations that don't get caught
    if word.endswith(('arás', 'arán')):
        possible_stems += stems(word[:-2])
    if word.endswith(('ara', 'ará')):
        possible_stems += stems(word[:-1])
    if word.endswith(('gué')):
        possible_stems += stems(word[:-3] + 'gar')
    if word.endswith(('ió', 'ía')):
        possible_stems += stems(word[:-2] + 'er')
        possible_stems += stems(word[:-2] + 'ir')
    if word.endswith(('ían')):
        possible_stems += stems(word[:-3] + 'er')
        possible_stems += stems(word[:-3] + 'ir')
    if word.endswith(('iéndo')):
        possible_stems += stems(word[:-5] + 'er')
        possible_stems += stems(word[:-5] + 'ir')
    if word.endswith(('é', 'ó')):
        possible_stems += stems(word[:-1] + 'ar')
    if word.endswith(('ár')):
        possible_stems += stems(word[:-2] + 'ar')
    if word.endswith(('cé')):
        possible_stems += stems(word[:-2] + 'zar')
    if word.endswith(('aran', 'aron', 'ándo')):
        possible_stems += stems(word[:-4] + 'ar')
    return possible_stems

def cached_stems(word):
    if word in _cache:
        return _cache[word]
    return None

def add_stem(word, stem):
    global _cache
    if word in _cache:
        _cache[word].append(stem)
    else:
        _cache[word] = [stem]

def stems(word):
    global _cache
    if word in _cache:
        return _cache[word]
    guesses = set()
    for meaning in _meanings(word):
        meaning = meaning.strip(')').strip('.')
        words = meaning.split()
        if len(words) > 2 and words[-2] == 'of':
            guesses.add(words[-1])
    if not guesses:
        if _translations(word):
            guesses.add(word)
        else:
            guesses.update(core_stems(word))
    _cache[word] = list(guesses)
    return _cache[word]
