from collections import Counter
import json
import pickle
import requests

# with open('known.p') as infile:
#     known = pickle.load(infile)
# with open('stems.p') as infile:
#     stems = pickle.load(infile)

def symbol_frequency(text):
    symbols = Counter()
    for letter in text:
        symbols[letter] += 1
    return symbols.most_common()

keep_chars = ['a', 'e', 'o', 'n', 's', 'r', 'i', 'l', 'd', 'u', 'c',
              't', 'm', '́', 'p', 'b', 'q', 'v', 'g', 'h', 'y', 'f',
              'j', 'z', '̃', 'x', '̈', 'w', 'k', ' ', '\n', 'í',  'ó',
              'á', 'é', 'ñ', 'ú', 'ü']

def clean_text(text):
    text = text.lower()
    translation_table = {}
    for s, _ in symbol_frequency(text):
        if s not in keep_chars:
            translation_table[ord(s)] = None
    return text.translate(translation_table)

def tokens(text):
    return clean_text(text).split()

def word_frequency(words):
    counter = Counter()
    for word in words:
        counter[word] += 1
    return counter

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
