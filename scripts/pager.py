from collections import Counter
import json
import pickle
import requests

def symbol_frequency(text):
    return Counter(text).most_common()

keep_chars = ['a', 'e', 'o', 'n', 's', 'r', 'i', 'l', 'd', 'u', 'c',
              't', 'm', '́', 'p', 'b', 'q', 'v', 'g', 'h', 'y', 'f',
              'j', 'z', '̃', 'x', '̈', 'w', 'k', ' ', '\n', 'í',  'ó',
              'á', 'é', 'ñ', 'ú', 'ü']

fuse_table = {'́a':'á', '́e':'é', '́i':'í', '́o':'ó', '́u':'ú', '̃n':'ñ', '̈u':'ü',
    '́á':'á', '́é':'é', '́í':'í', '́ó':'ó', '́ú':'ú', '̃ñ':'ñ', '̈ü':'ü'}

def fuse_accents(text):
    for i in range(len(text)):
        c = text[i]
        if c in ('́', '̃', '̈'):
            continue
        if i < len(text)-1:
            n = text[i+1]
            if n in ('́', '̃', '̈'):
                c = fuse_table.get(n + c, c)
        if c in keep_chars:
            yield c

def clean_text(text):
    return ''.join(l for l in fuse_accents(text.lower()))

def tokens(text):
    return clean_text(text).split()

def tokens_from_file(filename):
    with open(filename, encoding='utf-8') as infile:
        return tokens(infile.read())

def word_frequency(words):
    return Counter(words)

def word_info(word):
    'Use GlobeAPI and user assistance to get information on a word.'
    payload = {'from': 'spa', 'dest': 'eng', 'format': 'json', 'phrase': word}
    r = requests.get('https://glosbe.com/gapi/translate', params=payload)
    result = r.json()
    translations = []
    meanings = []
    if 'tuc' in result:
        for tuc in result['tuc']:
            if 'phrase' in tuc:
                translations.append(tuc['phrase']['text'])
            if 'meanings' in tuc:
                for meaning in tuc['meanings']:
                    meanings.append(meaning['text'])
    return translations, meanings

def guess_stem(word):
    translations, meanings = word_info(word)
    guesses = set()
    for meaning in meanings:
        meaning = meaning.strip('.')
        words = meaning.split()
        if len(words) > 3 and words[-3] == 'form' and words[-2] == 'of':
            guesses.add(words[-1])
    if translations and not guesses:
        guesses.add(word)
    return list(guesses)
