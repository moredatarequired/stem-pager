from collections import Counter
import pager
import stem_word
import sys

BOOK = None
#BOOK = 'el principito.txt'
#BOOK = 'hp1.txt'
#BOOK = '100years.txt'
#BOOK = 'Paulo Coelho - El Alquimista.txt'
#BOOK = 'huge.txt'
if BOOK is None:
    BOOK = sys.argv[1]

print('examining', BOOK)

with open(BOOK, encoding='utf-8') as infile:
    text = pager.tokens(infile.read())

ordered_words = pager.word_frequency(text)
stems = set()
known, unknown = 0, 0
for word, count in ordered_words.most_common():
    stem = stem_word.cached_stems(word)
    if stem is None:
        unknown += count
    else:
        stems.update(stem)
        known += count

print(len(text), 'words')
print(len(ordered_words), 'unique forms')
print(len(stems), 'known stems')
print(unknown, 'unknown,', known, 'known')

stem_count = Counter()
stem_count['--unstemmed words--'] = 0
for word, count in ordered_words.most_common():
    stem = stem_word.cached_stems(word)
    if stem is not None:
        if not stem:
            stem_count['--unstemmed words--'] += count
        for s in stem:
            stem_count[s] += count / len(stem)
    else:
        stem_count[word] += count

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

stats = cumulative_stats(stem_count, len(text))
for mark in [0.25, 0.5, 0.75, 0.85, 0.9, 0.925, 0.95, 0.965, 0.98, 0.99, 0.999]:
    print(mark, benchmark(stats, mark))

with open('words.txt', encoding='utf-8') as infile:
    known = pager.tokens(infile.read())

last_count = stem_count.most_common(1)[0][1] + 1
for stem, count in stem_count.most_common(100):
    if stem not in known:
        if last_count > count:
            last_count = count
            print('({})'.format(count))
        print(stem)
