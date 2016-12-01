from collections import Counter, defaultdict
from nltk.stem.snowball import SpanishStemmer
import pager
import sys

TEXT = sys.argv[1]
with open(TEXT, encoding='utf-8') as infile:
    text = pager.tokens(infile.read())
words = Counter(text)

stemmer = SpanishStemmer()
stem_counts = Counter()
stem_sources = defaultdict(Counter)
for word, count in words.most_common():
    stem = stemmer.stem(word)
    stem_counts[stem] += count
    stem_sources[stem][word] += count

def infinitive(word_count_list):
    for word, _ in word_count_list:
        if word.endswith(('ar', 'er', 'ir')):
            return word
    return None

def singular(word_count_list):
    words = [w for w, _ in word_count_list]
    min_length = min(len(w) for w in words)
    short_words = [w for w in words if len(w) == min_length]
    for word in short_words:
        if word.endswith('o'):
            return word
    return short_words[0]

def source_words(count_list):
    words = [count_list[0][0]]
    sing = singular(count_list)
    if sing not in words:
        words.append(sing)
    inf = infinitive(count_list)
    if inf and inf not in words:
        words.append(inf)
    return words

def cumulative_stats(frequencies, total):
    table = []
    covered = 0
    for word, count in frequencies.most_common():
        covered += count
        table.append((word, count, count / total, covered / total))
    return table

def benchmark(stats, coverage=0.95):
    for i, item in enumerate(stats):
        if item[3] > coverage:
            return i + 1, item[1]

stats = cumulative_stats(stem_counts, len(text))
for mark in [0.25, 0.5, 0.75, 0.85, 0.9, 0.925, 0.95, 0.965, 0.98, 0.99, 0.999]:
    print(mark, benchmark(stats, mark))

sc = len(stem_counts) // 100
for stem, count in stem_counts.most_common()[:5000:50]:
    #print(count, ' '.join(source_words(stem_sources[stem].most_common())))
    print(count, stem_sources[stem].most_common())
