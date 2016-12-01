from collections import Counter, defaultdict
import counter_stats
from nltk.stem.snowball import SpanishStemmer
import math
import pager
import sys

lemma_stems = dict()
with open('stem_to_lemma.txt', encoding='utf-8') as infile:
    for line in infile:
        stem, lemma_counts = line.split(' : ')
        lemma_stems[stem] = []
        for lemma_count in lemma_counts.split():
            lemma, freq = lemma_count.split('*')
            lemma_stems[stem].append((lemma, float(freq)))

def examine(filename):
    with open(filename, encoding='utf-8') as infile:
        text = pager.tokens(infile.read())
        words = Counter(text)

    stemmer = SpanishStemmer()
    lemma_counts = Counter()
    for word, count in words.most_common():
        stem = stemmer.stem(word)
        if stem not in lemma_stems:
            continue
        for lemma, freq in lemma_stems[stem]:
            if freq > 0.9 or freq * count > 1:
                lemma_counts[lemma] += math.ceil(freq * count)
    return lemma_counts
