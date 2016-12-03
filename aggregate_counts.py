from collections import Counter, defaultdict
import counter_stats
import sys

author_counts = defaultdict(Counter)
works = defaultdict(set)
for filename in sys.argv[1:]:
    author = filename.split(' - ')[0]
    with open(filename) as infile:
        for line in infile:
            parts = line.split('\t')
            if len(parts) != 3:
                continue
            count, lemma, sentence = parts
            author_counts[author][lemma] += int(count)
            works[lemma].add(author)
    print('processed', filename)

if len(author_counts) < 2:
    for v in author_counts.values():
        counter_stats.full_table(v)
    sys.exit()

total = Counter()
for counts in author_counts.values():
    total.update(counter_stats.normalize_counter(counts))

for word, authors in works.items():
    if len(authors) <= 1:
        del total[word]

counter_stats.full_table(total)
