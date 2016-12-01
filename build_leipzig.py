from collections import Counter, defaultdict
import counter_stats
from nltk.stem.snowball import SpanishStemmer
import pager
import pickle
import sys

word_file = 'leipzig_words.txt'

def word_and_count(line):
    parts = line.split()[1:] # first part is index (unneeded)
    count = int(parts[-1])
    word = pager.clean_text(' '.join(parts[:-1])).strip()
    return word, count

stemmer = SpanishStemmer()
word_collection = defaultdict(Counter)
with open(word_file) as infile:
    for line in infile:
        word, count = word_and_count(line)
        if not word or not count:
            continue
        stem = stemmer.stem(word)
        word_collection[stem][word] += count

for stem, counter in word_collection.items():
    word_collection[stem] = counter_stats.normalize_counter(counter)

with open('.leipzig_word_counts.p', 'wb') as outfile:
    pickle.dump(word_collection, outfile)
