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

def stem(word):
    global _cache
    if word in _cache:
        return _cache[word]
    guesses = set()
    for meaning in _meanings(word):
        meaning = meaning.strip('.')
        words = meaning.split()
        if len(words) > 2 and words[-2] == 'of':
            guesses.add(words[-1])
    if _translations(word) and not guesses:
        guesses.add(word)
    if len(guesses) > 1:
        print(word, guesses)
    if len(guesses) > 0:
        _cache[word] = list(guesses)[0]
    else:
        _cache[word] = None
    return _cache[word]
